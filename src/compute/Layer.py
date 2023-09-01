# coding: utf-8

from __future__ import division
from os.path import join
import shutil
from copy import deepcopy
from typing import Tuple

import jsonschema

from supervisely import ProjectMeta, TagMeta, ObjClass, TagMetaCollection, Annotation
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.utils import json_utils
from src.compute.utils import os_utils
from src.compute.utils.stat_timer import TinyTimer, global_timer
from supervisely.sly_logger import logger
from supervisely.annotation.json_geometries_map import GET_GEOMETRY_FROM_STR
from supervisely.imaging.color import hex2rgb

from src.compute.classes_utils import ClassConstants


def maybe_wrap_in_list(v):
    return v if isinstance(v, list) else [v]


def check_connection_name(connection_name):
    if len(connection_name) == 0:
        raise RuntimeError("Connection name should be non empty.")
    if connection_name[0] != "$" and connection_name != Layer.null:
        raise RuntimeError('Connection name should be "%s" or start with "$".' % Layer.null)


class Layer:
    null = "null"

    base_params = {
        "definitions": {
            "connections": {"type": "array", "items": {"type": "string"}, "minItems": 0},
            "color": {
                "type": "array",
                "items": {"type": "integer", "minimum": 0, "maximum": 255},
                "maxItems": 3,
                "minItems": 3,
            },
            "probability": {"type": "number", "minimum": 0, "maximum": 1},
            "percent": {"type": "number", "minimum": 0, "maximum": 100},
        },
        "type": "object",
        "required": ["action", "src", "dst"],
        "properties": {
            "action": {"type": "string"},
            "src": {"$ref": "#/definitions/connections"},
            "dst": {"type": "string"},
        },
    }

    layer_settings_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "required": {"type": "array", "items": {"type": "string", "enum": ["settings"]}},
            "properties": {
                "type": "object",
                "properties": {"settings": {}, "src": {}, "dst": {}},
                "required": ["settings"],
                "additionalProperties": False,
            },
        },
    }

    actions_mapping = {}

    def __init__(self, config):
        self._config = deepcopy(config)

        self.srcs = maybe_wrap_in_list(config["src"])
        self.dsts = maybe_wrap_in_list(config["dst"])

        self.settings = config.get("settings", {})

        self.cls_mapping = {}
        self.define_classes_mapping()
        self.output_meta = None

    def validate(self):
        jsonschema.validate(self._config, self.params)
        self.validate_source_connections()
        self.validate_dest_connections()

    @property
    def config(self):
        return deepcopy(self._config)

    def define_classes_mapping(self):
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def get_added_tag_metas(self):
        return []

    def get_removed_tag_metas(self):
        return []

    def is_archive(self):
        raise NotImplementedError()

    def requires_image(self):
        return False

    def validate_source_connections(self):
        for src in self.srcs:
            if src == Layer.null:
                raise RuntimeError('"%s" cannot be in "src".' % Layer.null)
            check_connection_name(src)

    def validate_dest_connections(self):
        for dst in self.dsts:
            check_connection_name(dst)

    # input_metas_dict: src datalevel name -> meta for the datalevel
    def make_output_meta(self, input_metas_dict):
        try:
            # if len(self.cls_mapping) == 0:
            #     raise RuntimeError("Empty cls_mapping for layer: {}".format(self.action))

            full_input_meta = ProjectMeta()
            for inp_meta in input_metas_dict.values():
                for inp_obj_class in inp_meta.obj_classes:
                    existing_obj_class = full_input_meta.obj_classes.get(inp_obj_class.name, None)
                    if existing_obj_class is None:
                        full_input_meta = full_input_meta.add_obj_class(inp_obj_class)
                    elif existing_obj_class.geometry_type != inp_obj_class.geometry_type:
                        raise RuntimeError(
                            f"Trying to add new class ({inp_obj_class.name}) with shape ({inp_obj_class.geometry_type.geometry_name()}). Same class with different shape ({existing_obj_class.geometry_type.geometry_name()}) exists."
                        )
                for inp_tag_meta in inp_meta.tag_metas:
                    existing_tag_meta = full_input_meta.tag_metas.get(inp_tag_meta.name, None)
                    if existing_tag_meta is None:
                        full_input_meta = full_input_meta.add_tag_meta(inp_tag_meta)
                    elif not existing_tag_meta.is_compatible(inp_tag_meta):
                        raise RuntimeError(
                            f"Trying to add new tag ({inp_tag_meta.name}) with type ({inp_tag_meta.value_type}) and possible values ({inp_tag_meta.possible_values}). Same tag with different type ({existing_tag_meta.value_type}) or possible values ({existing_tag_meta.possible_values}) exists."
                        )

            res_meta = deepcopy(full_input_meta)
            in_class_titles = set((obj_class.name for obj_class in full_input_meta.obj_classes))

            # __other__ -> smth
            if ClassConstants.OTHER in self.cls_mapping:
                other_classes = in_class_titles - set(self.cls_mapping.keys())
                for oclass in other_classes:
                    self.cls_mapping[oclass] = self.cls_mapping[ClassConstants.OTHER]
                del self.cls_mapping[ClassConstants.OTHER]

            missed_classes = in_class_titles - set(self.cls_mapping.keys())
            if len(missed_classes) != 0:
                raise RuntimeError("Some classes in mapping are missed: {}".format(missed_classes))

            for src_class_title, dst_class in self.cls_mapping.items():
                # __new__ -> [ list of classes ]
                if src_class_title == ClassConstants.NEW:
                    if type(dst_class) is not list:
                        raise RuntimeError("Internal class mapping error in layer (NEW spec).")
                    for new_cls_dict in dst_class:
                        new_name = new_cls_dict["title"]
                        new_shape = new_cls_dict["shape"]
                        new_geometry_type = GET_GEOMETRY_FROM_STR(new_shape)
                        if res_meta.obj_classes.has_key(new_name):
                            existing_cls = res_meta.obj_classes.get(new_name)
                            if existing_cls.geometry_type != new_geometry_type:
                                raise RuntimeError(
                                    f"Trying to add new class ({new_name}) with shape ({new_shape}). Same class with different shape ({existing_cls.geometry_type.geometry_name()}) exists."
                                )
                        else:
                            new_cls = ObjClass(new_name, new_geometry_type)
                            res_meta = res_meta.add_obj_class(new_cls)

                # __clone__ -> dict {parent_cls_name: child_cls_name}
                elif src_class_title == ClassConstants.CLONE:
                    if type(dst_class) is not dict:
                        raise RuntimeError("Internal class mapping error in layer (CLONE spec).")

                    for src_title, dst_title in dst_class.items():
                        real_src_cls = full_input_meta.obj_classes.get(src_title, None)
                        if real_src_cls is None:
                            raise RuntimeError(
                                'Class mapping error, source class "{}" not found.'.format(
                                    src_title
                                )
                            )
                        real_dst_cls = real_src_cls.clone(name=dst_title)
                        res_meta = res_meta.add_obj_class(real_dst_cls)

                elif src_class_title == ClassConstants.UPDATE:
                    if type(dst_class) is not list:
                        raise RuntimeError("Internal class mapping error in layer (NEW spec).")

                    for cls_dct in dst_class:
                        title = cls_dct["title"]
                        existing_class = res_meta.obj_classes.get(title, None)
                        if existing_class is not None:
                            new_shape = cls_dct.get("shape", None)
                            new_geometry_type = (
                                GET_GEOMETRY_FROM_STR(new_shape) if new_shape else None
                            )
                            new_color = cls_dct.get("color", None)
                            if new_color is not None and new_color[0] == "#":
                                new_color = hex2rgb(new_color)
                            new_obj_cls = existing_class.clone(
                                name=title, geometry_type=new_geometry_type, color=new_color
                            )
                            res_meta = res_meta.delete_obj_class(title)
                            res_meta = res_meta.add_obj_class(new_obj_cls)
                        else:
                            raise RuntimeError("Can not update class {}. Not found".format(title))

                # smth -> __default__
                elif dst_class == ClassConstants.DEFAULT:
                    pass

                # smth -> __ignore__
                elif dst_class == ClassConstants.IGNORE:
                    res_meta = res_meta.delete_obj_class(src_class_title)

                # smth -> new name
                elif type(dst_class) is str:
                    obj_cls = res_meta.get_obj_class(src_class_title)
                    obj_cls = obj_cls.clone(name=dst_class)
                    res_meta = res_meta.delete_obj_class(src_class_title)
                    res_meta = res_meta.add_obj_class(obj_cls)

                # smth -> new cls description
                elif type(dst_class) is dict:
                    new_name = dst_class.get("title", None)
                    new_shape = dst_class.get("shape", None)
                    new_geometry_type = GET_GEOMETRY_FROM_STR(new_shape) if new_shape else None
                    new_color = dst_class.get("color", None)
                    if new_color is not None and new_color[0] == "#":
                        new_color = hex2rgb(new_color)
                    obj_cls = res_meta.get_obj_class(src_class_title)
                    obj_cls = obj_cls.clone(
                        name=new_name, geometry_type=new_geometry_type, color=new_color
                    )
                    res_meta = res_meta.delete_obj_class(src_class_title)
                    res_meta = res_meta.add_obj_class(obj_cls)

            # TODO switch to get added / removed tags to be TagMeta instances.
            rm_imtags = [TagMeta.from_json(tag) for tag in self.get_removed_tag_metas()]
            res_meta = res_meta.clone(
                tag_metas=[tm for tm in res_meta.tag_metas if tm not in rm_imtags]
            )
            new_imtags = [TagMeta.from_json(tag) for tag in self.get_added_tag_metas()]
            new_imtags_exist = [
                tm for tm in res_meta.tag_metas.intersection(TagMetaCollection(new_imtags))
            ]
            # new_imtags_exist = res_meta.tags.intersection(new_imtags).to_list()
            if len(new_imtags_exist) != 0:
                exist_tag_names = [t.name for t in new_imtags_exist]
                logger.warn("Tags {} already exist.".format(exist_tag_names))
            res_meta.clone(tag_metas=new_imtags)
            self.output_meta = res_meta
        except Exception as e:
            logger.error(
                "Meta-error occurred in layer '{}' with config: {}".format(
                    self.action, self._config
                )
            )
            raise e

        return self.output_meta

    # def verbose_pre_start(self, total):
    #     shared_utils.e(self, '%d elements to process.' % total, 'INFO')
    #     self.total_samples = total
    #
    # verbose_interval = 100
    #
    # def get_total(self):
    #     if hasattr(self, 'total_samples'):
    #         return self.total_samples
    #     else:
    #         return -1
    #
    # def verbose_process(self, cur, name='', dataset_name=''):
    #     total = self.get_total()
    #     if shared_utils.IS_PROD() and total != -1 and hasattr(self, 'step') and hasattr(self, 'steps'):
    #         msg = 'Processed sample "%s" from dataset "%s"' % (name, dataset_name)
    #         logger.info(msg, extra={'progress': {
    #             'name': 'DATA_LAYER',
    #             'step': self.step,
    #             'steps': self.steps,
    #             'current': cur,
    #             'total': total,
    #         }})
    #     else:
    #         if cur % Layer.verbose_interval == 0:
    #             shared_utils.e(self,
    #                     'Processed %d%s elements.' % (cur,
    #                                                  '' if total == -1 else
    #                                                  '/%d (%.2f%%)' % (total, 100 * cur / total)),
    #                     'INFO')
    #
    # def verbose_post_start(self, cur):
    #     total = self.get_total()
    #     shared_utils.e(self,
    #             'Done processing %d%s elements.' % (cur,
    #                                                '' if total == -1 else
    #                                                '/%d (%.2f%%)' % (total, 100 * cur / total)),
    #             'INFO')

    def description(self):
        return 'action: "%s", src: %s, dst: %s' % (
            self.__class__.action,
            "[%s]" % ", ".join(map(lambda x: '"%s"' % x, self.srcs)),
            "[%s]" % ", ".join(map(lambda x: '"%s"' % x, self.dsts)),
        )

    def preprocess(self):
        pass

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        raise NotImplementedError()

    def process_timed(self, data_el: Tuple[ImageDescriptor, Annotation]):
        tm = TinyTimer()
        for layer_output in self.process(data_el):
            global_timer.add_value(self.__class__.action, tm.get_sec())
            tm = TinyTimer()
            yield layer_output

    @staticmethod
    def get_params(cls):
        if cls == Layer:
            raise RuntimeError("Class Layer has no params.")
        else:
            if not hasattr(cls, "layer_settings"):
                raise RuntimeError('Layer "%s" has no attribute "layer_settings"' % cls.__name__)

        layer_params = deepcopy(Layer.base_params)

        layer_params["properties"]["action"]["enum"] = [cls.action]

        layer_params["required"] += cls.layer_settings.get("required", [])
        layer_params["properties"].update(cls.layer_settings.get("properties", dict()))

        # print cls.action, layer_params['properties']

        layer_params = add_false_additional_properties(layer_params)

        return layer_params

    @staticmethod
    def dump_schemas(output_path):
        output_path = join(output_path, "schemas")
        shutil.rmtree(output_path)
        layers_output_path = join(output_path, "layers")
        os_utils.mkdir(layers_output_path)
        global_schema = {"definitions": deepcopy(Layer.base_params["definitions"])}
        global_schema["definitions"]["layers"] = dict()
        global_schema["items"] = {"anyOf": []}
        # global_schema['items']['minItems'] = 1
        # global_schema['items']['maxItems'] = 1

        for action, cls in Layer.actions_mapping.items():
            layer_schema = deepcopy(cls.params)
            json_utils.json_dump(
                layer_schema, join(layers_output_path, "%s.json" % (action)), indent=4
            )
            del layer_schema["definitions"]
            global_schema["definitions"]["layers"][action] = layer_schema
            global_schema["items"]["anyOf"].append({"$ref": "#/definitions/layers/%s" % action})

        json_utils.json_dump(global_schema, join(output_path, "schema.json"), indent=4)

    @staticmethod
    def register_layer(cls, type):
        if not hasattr(cls, "action"):
            raise RuntimeError('Layer "%s" has no attribute "action"' % cls.__name__)
        action = cls.action
        if action in Layer.actions_mapping:
            raise RuntimeError('Duplicate action "%s"' % action)

        jsonschema.validate(cls.layer_settings, Layer.layer_settings_schema)
        Layer.actions_mapping[action] = cls
        cls.params = Layer.get_params(cls)
        cls.type = type

    # def get_folder_from_ann(self, ann, tag2folder):
    #     img_info = shared_utils.get_img_info(ann)
    #     if len(ann.tags) == 0:
    #         raise RuntimeError('No tags found for %s.' % img_info)
    #     if ann.tags[-1] not in tag2folder:
    #         raise RuntimeError('No mapping for tag "%s" for %s.' % (ann.tags[-1], img_info))
    #     folder = tag2folder[ann.tags[-1]]
    #     return folder


def add_false_additional_properties(params):
    if type(params) == dict:
        for el in params:
            params[el] = add_false_additional_properties(params[el])
    if type(params) == list:
        for i in range(len(params)):
            params[i] = add_false_additional_properties(params[i])
    if type(params) == dict:
        if "required" in params:
            params["additionalProperties"] = False
    return params

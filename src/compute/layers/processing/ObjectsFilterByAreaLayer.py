# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Label, Tag, logger
from src.compute.dtl_utils import apply_to_labels


class ObjectsFilterByAreaLayer(Layer):
    action = "objects_filter_by_area"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes", "area", "comparator", "action", "tags_to_add"],
                "properties": {
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "area": {"type": ["integer", "string", "null"], "minimum": 0},
                    "comparator": {"type": "string", "enum": ["lt", "gt"]},
                    "action": {"type": "string", "enum": ["delete", "keep", "add_tags"]},
                    "tags_to_add": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "value"],
                            "properties": {
                                "name": {"type": "string"},
                                "value": {"type": ["string", "integer", "null"]},
                            },
                        },
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        if not self.net.preview_mode:
            if len(self.settings["classes"]) == 0:
                raise ValueError("Classes are not selected in Objects Filter By Area layer")
            if self.settings["action"] == "add_tags" and len(self.settings["tags_to_add"]) == 0:
                raise ValueError(
                    "Action is set to 'Add tags` in Objects Filter By Area layer, but tags are not selected"
                )
        super().validate()

    def modifies_data(self):
        return True

    def requires_item(self):
        return False

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        settings = self.settings
        classes = settings["classes"]
        area = settings["area"]
        comparator = settings["comparator"]
        action = settings["action"]

        def create_tags(tags_data: List[dict]):
            tags = []
            for tag_data in tags_data:
                tag_meta = self.output_meta.get_tag_meta(tag_data["name"])
                if tag_meta is None:
                    logger.debug(f"Tag {tag_data['name']} not found in output meta")
                    continue
                tag = Tag(tag_meta, tag_data["value"])
                tags.append(tag)
            return tags

        if action == "add_tags":
            tags = settings["tags_to_add"]
            tags = create_tags(tags)
        else:
            tags = []

        def filtered_delete_area_pixels(label: Label):
            if comparator == "lt":
                compar = lambda x: x < area
            else:
                compar = lambda x: x > area

            if label.obj_class.name in classes:
                label_area = label.area
                if compar(label_area):  # satisfied condition
                    return []  # action 'delete'
            return [label]

        def filtered_keep_area_pixels(label: Label):
            if comparator == "lt":
                compar = lambda x: x < area
            else:
                compar = lambda x: x > area

            if label.obj_class.name in classes:
                label_area = label.area
                if compar(label_area):  # satisfied condition
                    return [label]  # action 'keep'
            return []

        def filtered_add_tags_area_pixels(label: Label):
            if comparator == "lt":
                compar = lambda x: x < area
            else:
                compar = lambda x: x > area

            if label.obj_class.name in classes:
                label_area = label.area
                if compar(label_area):
                    try:
                        label = label.add_tags(tags)
                    except:
                        for tag in tags:
                            try:
                                label = label.add_tag(tag)
                            except:
                                logger.debug(f"Failed to add tag {tag} to label {label}")
            return [label]

        if action == "delete":
            filter_func = filtered_delete_area_pixels
        elif action == "keep":
            filter_func = filtered_keep_area_pixels
        else:
            filter_func = filtered_add_tags_area_pixels

        ann = apply_to_labels(ann, filter_func)
        yield img_desc, ann

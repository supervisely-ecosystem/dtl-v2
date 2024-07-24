# coding: utf-8

from copy import copy
from src.compute.Layer import Layer
from typing import Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
import supervisely as sly
from supervisely import Bitmap, Annotation, ObjClass, ProjectMeta, Polygon

from src.compute.classes_utils import ClassConstants


class ImgAugStudioLayer(Layer):
    action = "imgaug_studio"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["pipeline", "shuffle", "classes_to_convert"],
                "properties": {
                    "pipeline": {
                        "type": "array",
                        "properties": {
                            "category": {"type": "string"},
                            "method": {"type": "string"},
                            "params": {"type": "object"},
                            "sometimes": {"type": "number"},
                            "python": {"type": "string"},
                        },
                        "required": ["category", "method", "params", "sometimes", "python"],
                    },
                    "shuffle": {"type": "boolean"},
                    "classes_to_convert": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)
        self.original_meta = ProjectMeta()

    def requires_item(self):
        return True

    def modifies_data(self):
        return True

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_to_convert"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Bitmap.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def modify_original_meta(self) -> ProjectMeta:
        modified_classes = [
            ObjClass(cls_name, Polygon) for cls_name in self.settings["classes_to_convert"]
        ]
        original_meta = ProjectMeta(obj_classes=modified_classes)
        output_meta = copy(self.output_meta)

        for obj_class in modified_classes:
            modified_obj_class = output_meta.get_obj_class(obj_class.name)
            if modified_obj_class is not None:
                output_meta = output_meta.delete_obj_class(modified_obj_class.name)

        original_meta = original_meta.merge(output_meta)
        return original_meta

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        pipeline = self.settings["pipeline"]
        shuffle = self.settings["shuffle"]

        if len(pipeline) == 0:
            yield (img_desc, ann)
        else:
            img = img_desc.item_data
            if self.original_meta != self.output_meta:
                self.original_meta = self.modify_original_meta()
            augs = sly.imgaug_utils.build_pipeline(pipeline, shuffle)
            _, res_img, res_ann = sly.imgaug_utils.apply(augs, self.original_meta, img, ann)
            new_img_desc = img_desc.clone_with_item(res_img)
            yield (new_img_desc, res_ann)

# coding: utf-8

from typing import Tuple

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class ColorClassLayer(Layer):
    action = "color_class"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_color_mapping"],
                "properties": {
                    "classes_color_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    }
                },
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def define_classes_mapping(self):
        classes_color_mapping = self.settings["classes_color_mapping"]
        self.cls_mapping[ClassConstants.UPDATE] = [
            {"title": class_name, "color": class_color}
            for class_name, class_color in classes_color_mapping.items()
        ]

        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        ann = Annotation.from_json(ann.to_json(), self.output_meta)
        yield img_desc, ann

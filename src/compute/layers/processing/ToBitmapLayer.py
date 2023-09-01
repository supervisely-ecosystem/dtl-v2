# coding: utf-8

from typing import Tuple
import numpy as np

from supervisely import Annotation, Label, Bitmap

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels


# converts ALL types to Bitmap
class LineToBitmapLayer(Layer):
    action = "line2bitmap"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_mapping", "width"],
                "properties": {
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    },
                    "width": {
                        "description_en": "Line width in pixels",
                        "description_ru": "Ширина линии в пикселях",
                        "type": "integer",
                        "minimum": 1,
                    },
                },
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_mapping"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Bitmap.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        thickness = self.settings["width"]

        def to_bitmap(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name, None)
            if new_title is None:
                return [label]

            bmp_to_draw = np.zeros(ann.img_size, np.uint8)
            label.geometry.draw(bmp_to_draw, color=1, thickness=thickness)
            new_obj_class = label.obj_class.clone(new_title, Bitmap)
            new_label = label.clone(geometry=Bitmap(bmp_to_draw), obj_class=new_obj_class)
            return [new_label]

        ann = apply_to_labels(ann, to_bitmap)
        yield img_desc, ann

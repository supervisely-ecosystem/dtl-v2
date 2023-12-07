# coding: utf-8

from typing import Tuple
import numpy as np
from supervisely import Bitmap, Annotation, Label, ObjClass

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


# converts ALL types to FigureBitmap
class RasterizeLayer(Layer):
    action = "rasterize"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_mapping"],
                "properties": {
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    }
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_mapping"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Bitmap.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        shape_hw = ann.img_size
        imsize_wh = shape_hw[::-1]

        rasterised_mask = np.zeros(shape_hw, dtype=np.uint16)
        key_to_label = {}

        new_labels = []

        for i, label in enumerate(ann.labels):
            if label.obj_class.name in self.settings["classes_mapping"]:
                label.draw(rasterised_mask, i + 1)
                key_to_label[i + 1] = label
            else:
                new_labels.append(label)

        for inst in np.unique(rasterised_mask)[1:]:
            mask = rasterised_mask == inst
            old_label = key_to_label[inst]
            old_label: Label
            new_obj_class = ObjClass(
                name=self.cls_mapping[old_label.obj_class.name]["title"], geometry_type=Bitmap
            )
            label = old_label.clone(geometry=Bitmap(mask), obj_class=new_obj_class)
            new_labels.append(label)

        ann = ann.clone(labels=new_labels)

        yield img_desc, ann

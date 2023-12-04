# coding: utf-8

from typing import Tuple

import cv2
import numpy as np

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


class AnonymizeLayer(Layer):
    action = "anonymize"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes", "type"],
                "properties": {
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "type": {"type": "string", "enum": ["blur", "color", "class_color"]},
                    "color": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img = img_desc.read_image()
        img = img.astype(np.uint8)

        anon_type = self.settings["type"]
        if anon_type == "blur":
            anon_img = cv2.GaussianBlur(img, ksize=(0, 0), sigmaX=50)
            anon_img = np.clip(anon_img, 0, 255).astype(np.uint8)
            anon_mask = np.zeros(img.shape, dtype=bool)
            for label in ann.labels:
                if label.obj_class.name in self.settings["classes"]:
                    label.draw(anon_mask, color=True)
            img[anon_mask == True] = anon_img[anon_mask == True]
        elif anon_type == "color":
            for label in ann.labels:
                if label.obj_class.name in self.settings["classes"]:
                    label.draw(img, color=self.settings["color"])
        elif anon_type == "class_color":
            for label in ann.labels:
                if label.obj_class.name in self.settings["classes"]:
                    label.draw(img, color=label.obj_class.color)

        new_img_desc = img_desc.clone_with_item(img)
        yield new_img_desc, ann

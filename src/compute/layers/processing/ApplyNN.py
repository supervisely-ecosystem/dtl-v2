# coding: utf-8

from typing import Tuple

import cv2
import numpy as np

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from supervisely.nn.inference import Session
from src.compute.classes_utils import ClassConstants
import src.globals as g


class ApplyNN(Layer):
    action = "apply_nn"

    # jsonschema
    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["session_id", "model_info", "classes", "apply_method"],
                "properties": {
                    "session_id": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
                    "model_info": {"type": "object"},
                    "classes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "shape"],
                            "properties": {
                                "name": {"type": "string"},
                                "shape": {"type": "string"},
                            },
                        },
                    },
                    "apply_method": {"type": "string", "enum": ["image", "roi"]},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def define_classes_mapping(self):
        # super().define_classes_mapping()

        for new_class in self.settings["classes"]:
            self.cls_mapping[new_class["name"]] = {
                "title": new_class["name"],
                "shape": new_class["shape"],
            }
            self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img = img_desc.read_image()
        img = img.astype(np.uint8)

        img_path = img_desc.info.img_path

        apply_method = self.settings["apply_method"]
        if apply_method == "image":
            session = Session(g.api, self.settings["session_id"])
            ann = session.inference_image_path(img_path)
        elif apply_method == "roi":
            pass

        new_img_desc = img_desc.clone_with_img(img)
        yield new_img_desc, ann

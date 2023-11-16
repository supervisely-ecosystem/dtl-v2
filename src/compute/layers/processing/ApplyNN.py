# coding: utf-8

from typing import Tuple
from os.path import exists
import cv2
import numpy as np

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from supervisely.nn.inference import Session
from src.compute.classes_utils import ClassConstants
import src.globals as g
from supervisely.io.fs import silent_remove
import supervisely as sly


class ApplyNN(Layer):
    action = "apply_nn"

    # jsonschema
    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["session_id", "model_info", "classes", "tags", "apply_method"],
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
                                "color": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "minItems": 3,
                                    "maxItems": 3,
                                    "default": [0, 0, 0],
                                    "description": "RGB color",
                                },
                            },
                        },
                    },
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "value_type"],
                            "properties": {
                                "name": {"type": "string"},
                                "value_type": {"type": "string"},
                                "color": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "minItems": 3,
                                    "maxItems": 3,
                                    "default": [0, 0, 0],
                                    "description": "RGB color",
                                },
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
                "color": new_class["color"],
            }
            self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img = img_desc.read_image()
        img = img.astype(np.uint8)

        if self.settings["session_id"] is None:
            yield img_desc, ann
        else:
            img_path = f"{img_desc.info.image_name}{img_desc.info.ia_data['image_ext']}"

            apply_method = self.settings["apply_method"]
            if apply_method == "image":
                sly.image.write(img_path, img)
                session = Session(g.api, self.settings["session_id"])
                ann = session.inference_image_path(img_path)

                # remove tags for now
                # labels = []
                # for label in ann.labels:
                #     label = label.clone(tags=[])
                #     labels.append(label)
                # ann = ann.clone(img_tags=[], labels=labels)
                if exists(img_path):
                    silent_remove(img_path)

            elif apply_method == "roi":
                pass

            new_img_desc = img_desc.clone_with_img(img)
            yield new_img_desc, ann

    def requires_image(self):
        return True

# coding: utf-8

from typing import List, Tuple
import cv2
import numpy as np

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.exceptions import BadSettingsError


class BlurLayer(Layer):
    action = "blur"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "oneOf": [
                    {
                        "type": "object",
                        "required": ["name", "sigma"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "enum": [
                                    "gaussian",
                                ],
                            },
                            "sigma": {
                                "type": "object",
                                "required": ["min", "max"],
                                "properties": {
                                    "min": {"type": "number", "minimum": 0.01},
                                    "max": {"type": "number", "minimum": 0.01},
                                },
                            },
                        },
                    },
                    {
                        "type": "object",
                        "required": ["name", "kernel"],
                        "properties": {
                            "name": {
                                "type": "string",
                                "enum": [
                                    "median",
                                ],
                            },
                            "kernel": {"type": "integer", "minimum": 3},
                        },
                    },
                ],
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True

    def validate(self):
        super().validate()
        if (self.settings["name"] == "median") and (self.settings["kernel"] % 2 == 0):
            raise BadSettingsError("Kernel for median blur must be odd")

        def check_min_max(dictionary, text):
            if dictionary["min"] > dictionary["max"]:
                raise BadSettingsError('"min" should be <= than "max" for "{}"'.format(text))

        if self.settings["name"] == "gaussian":
            check_min_max(self.settings["sigma"], "sigma")

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        img = img_desc.read_image()
        img = img.astype(np.uint8)
        if self.settings["name"] == "gaussian":
            sigma_b = self.settings["sigma"]
            sigma_value = np.random.uniform(sigma_b["min"], sigma_b["max"])
            res_img = cv2.GaussianBlur(img, ksize=(0, 0), sigmaX=sigma_value)
        elif self.settings["name"] == "median":
            res_img = cv2.medianBlur(img, ksize=self.settings["kernel"])
        else:
            raise NotImplementedError()

        img = np.clip(res_img, 0, 255).astype(np.uint8)
        new_img_desc = img_desc.clone_with_item(img)
        yield new_img_desc, ann

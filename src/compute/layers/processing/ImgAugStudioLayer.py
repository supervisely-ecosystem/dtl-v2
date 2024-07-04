# coding: utf-8

from src.compute.Layer import Layer
import numpy as np
from typing import Tuple
import imgaug.augmenters as iaa
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
import json


class ImgAugStudioLayer(Layer):
    action = "iaa_imgcorruptlike_blur"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["pipeline"],
                # "properties": {
                #     "option": {"type": "string"},
                #     "severity": {"type": "integer", "minimum": 1, "maximum": 5},
                # },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        pipeline_json = self.settings["pipeline"]
        pipeline = json.loads(pipeline_json)

        if self.settings["option"] == "defocus_blur":
            aug = iaa.imgcorruptlike.DefocusBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "motion_blur":
            aug = iaa.imgcorruptlike.MotionBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "zoom_blur":
            aug = iaa.imgcorruptlike.ZoomBlur(severity=self.settings["severity"])

        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

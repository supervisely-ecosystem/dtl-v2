# coding: utf-8

from src.compute.Layer import Layer
import numpy as np
from typing import Tuple
import imgaug.augmenters as iaa
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
import supervisely as sly

import json


class ImgAugStudioLayer(Layer):
    action = "imgaug_studio"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["pipeline", "shuffle"],
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
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        pipeline = self.settings["pipeline"]
        shuffle = self.settings["shuffle"]
        if len(pipeline) == 0:
            yield (img_desc, ann)
        else:
            img = img_desc.item_data
            meta = self.output_meta
            augs = sly.imgaug_utils.build_pipeline(pipeline, shuffle)
            _, res_img, res_ann = sly.imgaug_utils.apply(augs, meta, img, ann)
            new_img_desc = img_desc.clone_with_item(res_img)
            new_ann = res_ann
            yield (new_img_desc, new_ann)

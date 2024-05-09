# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation
import imgaug.augmenters as iaa
import numpy as np


class ElasticTransformLayer(Layer):
    action = "elastic_transform"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["severity"],
                "properties": {
                    "severity": {"type": "integer", "minimum": 1, "maximum": 5},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def modifies_data(self):
        return False

    def requires_item(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        aug = iaa.imgcorruptlike.ElasticTransform(severity=self.settings["severity"])
        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        raise NotImplementedError

    def has_batch_processing(self) -> bool:
        return False

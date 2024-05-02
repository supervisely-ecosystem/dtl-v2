# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation
import imgaug.augmenters as iaa
import numpy as np


class PixelateLayer(Layer):
    action = "pixelate"

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
        aug = iaa.imgcorruptlike.Pixelate(severity=self.settings["severity"])
        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        aug = iaa.imgcorruptlike.Pixelate(severity=self.settings["severity"])

        original_images = [item_desc.item_data for item_desc in item_descs]
        pixelated_images = aug.augment_images(original_images)

        if len(item_descs) == len(pixelated_images):
            for item_desc, pix_img in zip(item_descs, pixelated_images):
                item_desc.update_item(pix_img)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

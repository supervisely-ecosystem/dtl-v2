# coding: utf-8

import numpy as np
from typing import Tuple
import imgaug.augmenters as iaa
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.layers.processing.ImgCorruptLikeLayer import ImgCorruptLikeLayer


class ImgAugCorruptlikeCompressionLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_compression"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        if self.settings["option"] == "elastic_transform":
            aug = iaa.imgcorruptlike.ElasticTransform(severity=self.settings["severity"])
        elif self.settings["option"] == "pixelate":
            aug = iaa.imgcorruptlike.Pixelate(severity=self.settings["severity"])
        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

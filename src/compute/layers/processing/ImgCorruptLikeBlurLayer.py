# coding: utf-8

import numpy as np
from typing import Tuple
import imgaug.augmenters as iaa
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.layers.processing.ImgCorruptLikeLayer import ImgCorruptLikeLayer


class ImgAugCorruptlikeBlurLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_blur"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        if self.settings["option"] == "gaussian_blur":
            aug = iaa.imgcorruptlike.GaussianBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "glass_blur":
            aug = iaa.imgcorruptlike.GlassBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "defocus_blur":
            aug = iaa.imgcorruptlike.DefocusBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "motion_blur":
            aug = iaa.imgcorruptlike.MotionBlur(severity=self.settings["severity"])
        elif self.settings["option"] == "zoom_blur":
            aug = iaa.imgcorruptlike.ZoomBlur(severity=self.settings["severity"])

        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

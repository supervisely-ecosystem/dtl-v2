# coding: utf-8

from src.compute.Layer import Layer
import numpy as np
from typing import Tuple
import imgaug.augmenters as iaa
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


class ImgCorruptLikeLayer(Layer):
    action = "iaa_imgaug_corruptlike"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["severity"],
                "properties": {
                    "option": {"type": "string"},
                    "severity": {"type": "integer", "minimum": 1, "maximum": 5},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True


class ImgAugCorruptlikeBlurLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_blur"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

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


class ImgAugCorruptlikeColorLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_color"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        if self.settings["option"] == "contrast":
            aug = iaa.imgcorruptlike.Contrast(severity=self.settings["severity"])
        elif self.settings["option"] == "brightness":
            aug = iaa.imgcorruptlike.Brightness(severity=self.settings["severity"])
        elif self.settings["option"] == "saturate":
            aug = iaa.imgcorruptlike.Saturate(severity=self.settings["severity"])

        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)


class ImgAugCorruptlikeCompressionLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_compression"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        if self.settings["option"] == "jpeg_compression":
            aug = iaa.imgcorruptlike.JpegCompression(severity=self.settings["severity"])
        elif self.settings["option"] == "pixelate":
            aug = iaa.imgcorruptlike.Pixelate(severity=self.settings["severity"])
        elif self.settings["option"] == "elastic_transform":
            aug = iaa.imgcorruptlike.ElasticTransform(severity=self.settings["severity"])
        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)


class ImgAugCorruptlikeNoiseLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_noise"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        if self.settings["option"] == "gaussian_noise":
            aug = iaa.imgcorruptlike.GaussianNoise(severity=self.settings["severity"])
        elif self.settings["option"] == "shot_noise":
            aug = iaa.imgcorruptlike.ShotNoise(severity=self.settings["severity"])
        elif self.settings["option"] == "impulse_noise":
            aug = iaa.imgcorruptlike.ImpulseNoise(severity=self.settings["severity"])
        elif self.settings["option"] == "speckle_noise":
            aug = iaa.imgcorruptlike.SpeckleNoise(severity=self.settings["severity"])

        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)


class ImgAugCorruptlikeWeatherLayer(ImgCorruptLikeLayer):
    action = "iaa_imgcorruptlike_weather"

    def __init__(self, config, net):
        ImgCorruptLikeLayer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        if self.settings["option"] == "fog":
            aug = iaa.imgcorruptlike.Fog(severity=self.settings["severity"])
        elif self.settings["option"] == "frost":
            aug = iaa.imgcorruptlike.Frost(severity=self.settings["severity"])
        elif self.settings["option"] == "snow":
            aug = iaa.imgcorruptlike.Snow(severity=self.settings["severity"])
        elif self.settings["option"] == "spatter":
            aug = iaa.imgcorruptlike.Spatter(severity=self.settings["severity"])

        img = img_desc.read_image()
        pixelated_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(pixelated_img)
        yield (new_img_desc, ann)

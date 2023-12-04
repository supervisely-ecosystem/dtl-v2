# coding: utf-8

from typing import Tuple
import numpy as np
from supervisely import Annotation
from supervisely.aug.aug import resize

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.exceptions import BadSettingsError


class ResizeLayer(Layer):
    action = "resize"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["width", "height", "aspect_ratio"],
                "properties": {
                    "width": {"type": "integer", "minimum": -1},
                    "height": {"type": "integer", "minimum": -1},
                    "aspect_ratio": {
                        "type": "object",
                        "required": ["keep"],
                        "properties": {"keep": {"type": "boolean"}},
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        super().validate()
        if self.settings["height"] * self.settings["width"] == 0:
            raise BadSettingsError(self, '"height" and "width" should be != 0')
        if self.settings["height"] + self.settings["width"] == -2:
            raise BadSettingsError(self, '"height" and "width" cannot be both set to -1')
        if self.settings["height"] * self.settings["width"] < 0:
            if not self.settings["aspect_ratio"]["keep"]:
                raise BadSettingsError(
                    self,
                    '"keep" "aspect_ratio" should be set to "true" '
                    'when "width" or "height" is -1',
                )

    def requires_image(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img_hw = ann.img_size
        img = img_desc.read_image()

        keep = self.settings["aspect_ratio"]["keep"]
        set_size_hw = (self.settings["height"], self.settings["width"])

        def get_result_hw(img_hw: Tuple[int, int], set_hw: Tuple[int, int]) -> Tuple[int, int]:
            src_h, src_w = img_hw
            set_h, set_w = set_hw
            new_h, new_w = set_h, set_w
            if set_h == -1:
                scale = set_w / src_w
                new_h = int(round(src_h * scale))
                new_w = set_w
            elif set_w == -1:
                scale = set_h / src_h
                new_h = set_h
                new_w = int(round(src_w * scale))
            return new_h, new_w

        def get_resize_hw(
            img_hw: Tuple[int, int], set_hw: Tuple[int, int], keep: bool
        ) -> Tuple[int, int]:
            src_h, src_w = img_hw
            set_h, set_w = set_hw
            new_h, new_w = set_h, set_w
            if keep:
                if set_h == -1:
                    scale = set_w / src_w
                    new_h = int(round(src_h * scale))
                    new_w = set_w
                elif set_w == -1:
                    scale = set_h / src_h
                    new_h = set_h
                    new_w = int(round(src_w * scale))
                else:
                    scale_h = set_h / src_h
                    scale_w = set_w / src_w
                    if scale_h < scale_w:
                        scale = scale_h
                        new_h = set_h
                        new_w = int(round(src_w * scale))
                    else:
                        scale = scale_w
                        new_h = int(round(src_h * scale))
                        new_w = set_w

            return new_h, new_w

        def _get_res_image_shape(result_hw, img):
            if len(img.shape) > 2:
                return (*result_hw, img.shape[2])
            return result_hw

        def extend(
            img: np.ndarray, ann: Annotation, result_hw: Tuple[int, int]
        ) -> Tuple[np.ndarray, Annotation]:
            src_h, src_w = ann.img_size
            res_h, res_w = result_hw
            shift_x, shift_y = (res_w - src_w) // 2, (res_h - src_h) // 2

            res_img = np.zeros(_get_res_image_shape(result_hw, img), img.dtype)
            res_img[shift_y : shift_y + img.shape[0], shift_x : shift_x + img.shape[1]] = img

            shifted_labels = []
            for label in ann.labels:
                shifted_labels.append(label.translate(shift_y, shift_x))

            return res_img, ann.clone(img_size=res_img.shape[:2], labels=shifted_labels)

        img, ann = resize(img, ann, get_resize_hw(img_hw, set_size_hw, keep))
        img, ann = extend(img, ann, get_result_hw(ann.img_size, set_size_hw))
        new_img_desc = img_desc.clone_with_item(img)

        yield new_img_desc, ann

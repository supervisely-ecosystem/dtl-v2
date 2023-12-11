# coding: utf-8

from typing import Tuple
import numpy as np

from supervisely import Annotation, Rectangle
from supervisely import aug

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels
from src.exceptions import BadSettingsError


class RotateLayer(Layer):
    action = "rotate"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["rotate_angles", "black_regions"],
                "properties": {
                    "rotate_angles": {
                        "type": "object",
                        "required": ["min_degrees", "max_degrees"],
                        "properties": {
                            "min_degrees": {"type": "number"},
                            "max_degrees": {"type": "number"},
                        },
                    },
                    "black_regions": {
                        "type": "object",
                        "required": ["mode"],
                        "properties": {
                            "mode": {"type": "string", "enum": ["keep", "crop", "preserve_size"]}
                        },
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        super().validate()
        if (
            self.settings["rotate_angles"]["min_degrees"]
            > self.settings["rotate_angles"]["max_degrees"]
        ):
            raise BadSettingsError('"min_degrees" should be <= "max_degrees"')

    def requires_image(self):
        return True

    @staticmethod
    def expand_image_with_rect(img: np.ndarray, req_rect: Rectangle):
        src_im_rect = Rectangle.from_array(img)
        if src_im_rect.contains(req_rect):
            return img, (0, 0)

        src_ct = [int(x + 0.5) for x in src_im_rect.center]
        new_w2 = max(src_ct[0] - req_rect.left, req_rect.right - src_ct[0])
        new_h2 = max(src_ct[1] - req_rect.top, req_rect.bottom - src_ct[1])
        exp_w = max(src_im_rect.width, 2 * new_w2)
        exp_h = max(src_im_rect.height, 2 * new_h2)
        delta_x = (exp_w - src_im_rect.width) // 2
        delta_y = (exp_h - src_im_rect.height) // 2

        exp_img = np.zeros((exp_h, exp_w, img.shape[2]), dtype=img.dtype)
        exp_img[delta_y : delta_y + src_im_rect.height, delta_x : delta_x + src_im_rect.width] = img

        return exp_img, (delta_x, delta_y)

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        angle_dct = self.settings["rotate_angles"]
        min_degrees, max_degrees = angle_dct["min_degrees"], angle_dct["max_degrees"]
        rotate_degrees = np.random.uniform(min_degrees, max_degrees)

        if rotate_degrees == 0:
            return img_desc, ann

        black_reg_mode = self.settings["black_regions"]["mode"]

        if rotate_degrees == 90:
            pass

        if rotate_degrees == 180:
            pass

        img = img_desc.read_image()
        new_img, new_ann = aug.rotate(
            img,
            ann,
            degrees=rotate_degrees,
            mode=aug.RotationModes.CROP if black_reg_mode == "crop" else aug.RotationModes.KEEP,
        )
        if black_reg_mode == "preserve_size":
            rect_to_crop = Rectangle.from_array(img)
            new_img, (delta_x, delta_y) = self.expand_image_with_rect(new_img, rect_to_crop)

            top_pad = max((new_img.shape[0] - ann.img_size[0]) // 2, 0)
            lefet_pad = max((new_img.shape[1] - ann.img_size[1]) // 2, 0)
            new_img, new_ann = aug.crop(
                new_img,
                new_ann,
                top_pad=top_pad,
                bottom_pad=new_img.shape[0] - top_pad - ann.img_size[0],
                left_pad=lefet_pad,
                right_pad=new_img.shape[1] - lefet_pad - ann.img_size[1],
            )
            new_ann.clone(img_size=new_img.shape[:2])

            new_ann = apply_to_labels(new_ann, lambda x: [x.translate(delta_x, delta_y)])

        if new_img is None:
            return  # no yield

        yield img_desc.clone_with_item(new_img), new_ann

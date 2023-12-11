# coding: utf-8

from typing import Tuple

from supervisely import Annotation
from supervisely.geometry.sliding_windows import SlidingWindows
from supervisely.imaging.image import crop

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


class SlidingWindowLayer(Layer):
    action = "sliding_window"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["window", "min_overlap"],
                "properties": {
                    "window": {
                        "type": "object",
                        "required": ["height", "width"],
                        "properties": {
                            "height": {"type": "integer", "minimum": 1},
                            "width": {"type": "integer", "minimum": 1},
                        },
                    },
                    "min_overlap": {
                        "type": "object",
                        "required": ["x", "y"],
                        "properties": {
                            "x": {"type": "integer", "minimum": 0},
                            "y": {"type": "integer", "minimum": 0},
                        },
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_image(self):
        return True

    def modifies_data(self):
        return True

    def preprocess(self):
        window_wh = (self.settings["window"]["width"], self.settings["window"]["height"])
        min_overlap_xy = (self.settings["min_overlap"]["x"], self.settings["min_overlap"]["y"])
        self.sliding_windows = SlidingWindows(window_wh, min_overlap_xy)  # + some validating

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img_hw = ann.img_size
        img_orig = img_desc.read_image()

        for rect_to_crop in self.sliding_windows.get(img_hw):
            res_img = crop(img_orig, rect_to_crop)
            res_ann = ann.relative_crop(rect_to_crop)

            yield img_desc.clone_with_item(res_img), res_ann

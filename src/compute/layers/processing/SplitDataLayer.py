from src.compute.Layer import Layer
import numpy as np
from typing import Tuple
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
import supervisely as sly
from copy import deepcopy
from typing import List


class SplitDataLayer(Layer):
    action = "split_data"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["method"],
                "properties": {
                    "method": {
                        "type": "number",
                    }
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):

        def _split_by_percent(orig_ann):
            raise NotImplementedError

        def _split_by_num(orig_ann):
            raise NotImplementedError

        def _split_by_class(orig_ann):
            image_labels = orig_ann.labels
            if len(image_labels) > 0:
                classes = [label.obj_class for label in image_labels]
            raise NotImplementedError

        def _split_by_tags(orig_ann):
            image_tags = orig_ann.img_tags
            if len(image_tags) == 0:
                pass
            raise NotImplementedError

        idx_to_func = {
            0: _split_by_percent,
            1: _split_by_num,
            3: _split_by_class,
            4: _split_by_tags,
        }
        img_desc, orig_ann = data_el
        method_idx = self.settings.get("method", 0)
        meta = self.output_meta

        func = idx_to_func.get(method_idx)
        func(orig_ann)

        new_img_desc = deepcopy(img_desc)
        yield (new_img_desc, orig_ann)

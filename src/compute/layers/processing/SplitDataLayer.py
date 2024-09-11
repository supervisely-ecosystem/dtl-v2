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
        def _split() -> List[str]:
            pass

        method = self.settings.get("method", 0)
        img_desc, orig_ann = data_el
        # meta = self.output_meta

        new_img_desc = deepcopy(img_desc)
        yield (new_img_desc, orig_ann)

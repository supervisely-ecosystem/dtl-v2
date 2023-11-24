# coding: utf-8

from typing import Tuple

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


class FilterImageByObjectLayer(Layer):
    action = "filter_images_by_object"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["include", "exclude"],
                "properties": {
                    "include": {"type": "array", "items": {"type": "string"}},
                    "exclude": {"type": "array", "items": {"type": "string"}},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        satisfies_cond = True
        include_classes = self.settings["include"]
        exclude_classes = self.settings["exclude"]

        for label in ann.labels:
            if label.obj_class.name in exclude_classes:
                satisfies_cond = False
                break
            if label.obj_class.name not in include_classes:
                satisfies_cond = False
                break

        if satisfies_cond:
            yield data_el + tuple([0])  # branch 0
        else:
            yield data_el + tuple([1])  # branch 1

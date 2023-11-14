# coding: utf-8

from typing import Tuple

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class FilterImageByTagLayer(Layer):
    action = "filter_image_by_tag"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["tag", "condition"],
                "properties": {
                    "tag": {
                        "type": "object",
                        "required": ["name", "value"],
                        "properties": {
                            "name": {"type": "string"},
                            "value": {},
                        },
                    },
                    "condition": {"type": "string", "enum": ["with", "without"]},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        satisfies_cond = False
        condition = self.settings["condition"]
        tag_name = self.settings["tag"]["name"]
        tag_value = self.settings["tag"]["value"]

        if condition == "with":
            satisfies_cond = False
        elif condition == "without":
            satisfies_cond = True
        else:
            raise NotImplementedError()

        for img_tag in ann.img_tags:
            if img_tag.name == tag_name and img_tag.value == tag_value:
                satisfies_cond = not satisfies_cond
                break

        if satisfies_cond:
            yield data_el + tuple([0])  # branch 0
        else:
            yield data_el + tuple([1])  # branch 1

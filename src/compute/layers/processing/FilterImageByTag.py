# coding: utf-8

from typing import List, Tuple, Union

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from supervisely import Tag, TagCollection


class FilterImageByTagLayer(Layer):
    action = "filter_image_by_tag"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["tags", "condition"],
                "properties": {
                    "tags": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name", "value"],
                            "properties": {
                                "name": {"type": "string"},
                                "value": {},
                            },
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

        def has_tags(img_tags: Union[List[Tag], TagCollection], filter_tags: List[dict]):
            has_filters = [False for _ in filter_tags]
            for img_tag in img_tags:
                for i, f_tag in enumerate(filter_tags):
                    if img_tag.name == f_tag["name"] and img_tag.value == f_tag["value"]:
                        has_filters[i] = True
            return all(has_filters)

        if condition == "with":
            satisfies_cond = False
        elif condition == "without":
            satisfies_cond = True
        else:
            raise NotImplementedError()

        if has_tags(ann.img_tags, self.settings["tags"]):
            satisfies_cond = not satisfies_cond

        if satisfies_cond:
            yield data_el + tuple([0])  # branch 0
        else:
            yield data_el + tuple([1])  # branch 1

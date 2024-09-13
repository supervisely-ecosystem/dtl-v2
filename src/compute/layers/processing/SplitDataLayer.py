from src.compute.Layer import Layer
from collections import defaultdict
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
                "required": ["split_method", "split_ratio", "split_num"],
                "properties": {
                    "split_method": {
                        "type": "string",
                    },
                    "split_ratio": {"type": "number"},
                    "split_num": {"type": "number"},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        # Check if the selected split method is valid
        return super().validate()

    def requires_item(self):
        return False

    def modifies_data(self):
        return False

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        item_desc, ann = data_el
        total_items_cnt = self.net.get_total_elements()  # to split by num/percent
        item_idx = item_desc.get_item_idx()

        def _split_by_percent() -> List[Tuple[ImageDescriptor, Annotation]]:
            new_item_desc = deepcopy(item_desc)
            split_ratio = self.settings.get("split_ratio", 0.8)
            split_num = total_items_cnt * split_ratio
            split_index = int(item_idx / split_num) + (item_idx % split_num > 0)
            dataset = f"split_{split_index}"
            new_item_desc.res_ds_name = dataset
            return [(new_item_desc, ann)]

        def _split_by_num() -> List[Tuple[ImageDescriptor, Annotation]]:
            new_item_desc = deepcopy(item_desc)
            split_num = self.settings.get("split_num", total_items_cnt // 2)
            split_index = int(item_idx / split_num) + (item_idx % split_num > 0)
            print(f"ITEM INDEX: {item_idx}, SPLIT INDEX: {split_index}")
            dataset = f"split_{split_index}"
            new_item_desc.res_ds_name = dataset
            return [(new_item_desc, ann)]

        def _split_by_class() -> List[Tuple[ImageDescriptor, Annotation]]:
            new_item_desc = deepcopy(item_desc)

            image_labels = ann.labels
            if len(image_labels) > 0:
                classes = list({label.obj_class.name for label in image_labels})
                items = []
                for class_name in classes:
                    curr_item_desc = deepcopy(item_desc)
                    curr_item_desc.res_ds_name = class_name
                    items.append((curr_item_desc, ann))
                return items
            return [(new_item_desc, ann)]

        def _split_by_tags() -> List[Tuple[ImageDescriptor, Annotation]]:
            image_tags = list(set(ann.img_tags.keys()))
            label_tags = list(set([tag for label in ann.labels for tag in label.tags.keys()]))
            if len(image_tags) == 0 and len(label_tags) == 0:
                return [(item_desc, ann)]

            tag_names = set()
            items = []
            for img_tag_name in image_tags:
                if img_tag_name not in tag_names:
                    tag_names.add(img_tag_name)
                    new_img_item_desc = deepcopy(item_desc)
                    new_img_item_desc.res_ds_name = img_tag_name
                    items.append((new_img_item_desc, ann))
            for tag_name in label_tags:
                if tag_name not in tag_names:
                    tag_names.add(tag_name)
                    new_label_item_desc = deepcopy(item_desc)
                    new_label_item_desc.res_ds_name = tag_name
                    items.append((new_label_item_desc, ann))
            return items

        split_func_map = {
            "percent": _split_by_percent,
            "number": _split_by_num,
            "classes": _split_by_class,
            "tags": _split_by_tags,
        }
        split_method = self.settings.get("split_method", "percent")
        func = split_func_map.get(split_method)
        items = func()
        for item in items:
            yield item

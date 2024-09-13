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
        # Use to split data by percentage or number
        total_items_cnt = self.net.get_total_elements()
        item_idx = item_desc.get_item_idx()

        def _split_by_percent() -> List[Tuple[ImageDescriptor, Annotation]]:
            new_item_desc = deepcopy(item_desc)
            split_ratio = self.settings.get("split_ratio", 0.8)
            split_index = int(item_idx / (total_items_cnt * split_ratio))
            dataset = f"split_{split_index}"
            new_item_desc.res_ds_name = dataset
            return [(new_item_desc, ann)]

        def _split_by_num() -> List[Tuple[ImageDescriptor, Annotation]]:
            new_item_desc = deepcopy(item_desc)
            split_num = self.settings.get("split_num", total_items_cnt // 2)
            split_index = int(item_idx / split_num)
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
            image_tags = ann.img_tags
            if len(image_tags) > 0:
                img_tag_names = list({tag.name for tag in image_tags})
                label_tags_names = list({tag.name for label in ann.labels for tag in label.tags})
                # Check if tag is present on both image and object to avoid image duplication

                tag_names = set()
                items = []
                for img_tag_name in img_tag_names:
                    if img_tag_name not in tag_names:
                        tag_names.add(img_tag_name)
                        new_img_item_desc = deepcopy(item_desc)
                        new_img_item_desc.res_ds_name = img_tag_name
                        items.append((new_img_item_desc, ann))
                for label_tag_name in label_tags_names:
                    if label_tag_name not in tag_names:
                        tag_names.add(label_tag_name)
                        new_label_item_desc = deepcopy(item_desc)
                        new_label_item_desc.res_ds_name = label_tag_name
                        items.append((new_label_item_desc, ann))
                return items
            else:
                return [(item_desc, ann)]

        idx_to_func = {
            "percent": _split_by_percent,
            "number": _split_by_num,
            "classes": _split_by_class,
            "tags": _split_by_tags,
        }
        split_method = self.settings.get("split_method", "percent")
        func = idx_to_func.get(split_method)
        items = func()
        for item in items:
            yield item

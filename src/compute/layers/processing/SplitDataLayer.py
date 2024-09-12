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

    def validate(self):
        # Check if the selected split method is valid
        return super().validate()

    def requires_item(self):
        return False

    def modifies_data(self):
        return False

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        item_desc, ann = data_el
        new_item_desc = deepcopy(item_desc)

        split_method = self.settings.get("split_method", 0)
        # Use to split data by percentage or number
        total_items_cnt = self.net.get_total_elements()
        item_idx = item_desc.get_item_idx()

        def _split_by_percent() -> List[ImageDescriptor]:
            # change split_ratio to actual name
            split_ratio = self.settings.get("split_ratio", 0.8)
            split_index = int(item_idx / (total_items_cnt * split_ratio))
            dataset = f"split_{split_index}"
            new_item_desc.res_ds_name = dataset
            return [(new_item_desc, ann)]

        def _split_by_num() -> List[ImageDescriptor]:
            # change split_num to actual name
            split_num = self.settings.get("split_num", total_items_cnt // 2)
            split_index = int(item_idx / split_num)
            dataset = f"split_{split_index}"
            new_item_desc.res_ds_name = dataset
            return [(new_item_desc, ann)]

        def _split_by_class() -> List[ImageDescriptor]:
            image_labels = ann.labels
            if len(image_labels) > 0:
                classes = [label.obj_class.name for label in image_labels]
                classes = set(classes)
                for class_name in classes:
                    # create new new_item_desc for each iteration (not implemented)
                    new_item_desc.res_ds_name = class_name
            return  # list of tuples of ImageDescriptor and Annotation

        def _split_by_tags() -> List[ImageDescriptor]:
            image_tags = ann.img_tags
            if len(image_tags) > 0:
                img_tag_names = [tag.name for tag in image_tags]
                img_tag_names = set(img_tag_names)
                for img_tag_name in img_tag_names:
                    # create new new_item_desc for each iteration (not implemented)
                    new_item_desc.res_ds_name = img_tag_name
                for label in orig_ann.labels:
                    label_tags_names = [tag.name for tag in label.tags]
                    label_tags_names = set(label_tags_names)
                    for label_tag_name in label_tags_names:
                        # create new new_item_desc for each iteration (not implemented)
                        new_item_desc.res_ds_name = label_tag_name

            # !!!Check if tag is present on both image and object to avoid image duplication!!!
            return  # list of tuples of ImageDescriptor and Annotation

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
        new_img_desc = func(orig_ann)

        # Must yield output of split method
        yield (new_img_desc, orig_ann)

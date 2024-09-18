from src.compute.Layer import Layer
from typing import Tuple
from supervisely import Annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.exceptions import BadSettingsError
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
        split_method = self.settings["split_method"]
        split_ratio = self.settings["split_ratio"]
        split_num = self.settings["split_num"]

        allowed_methods = ["percent", "number", "classes", "tags"]

        if split_method not in allowed_methods:
            raise BadSettingsError(f"Unknown split method selected: {split_method}")
        if split_ratio < 1 or split_ratio > 100:
            raise BadSettingsError(f"Split percentage can not be equal to {split_ratio}")
        if split_num < 1 or split_num > 10000:
            raise BadSettingsError(f"Split number can not be equal to {split_num}")
        super().validate()

    def requires_item(self):
        return False

    def modifies_data(self):
        return False

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        def replace_ds_name(new_ds_name):
            new_item_desc = deepcopy(item_desc)
            new_item_desc.res_ds_name = new_ds_name
            new_item_desc.set_ds_info(None)
            return new_item_desc

        def _split_by_percent() -> List[Tuple[ImageDescriptor, Annotation]]:
            split_ratio = self.settings["split_ratio"]
            split_num = self.net.total_elements_cnt * (split_ratio / 100)
            split_index = int(item_idx / split_num) + (item_idx % split_num > 0)
            return [(replace_ds_name(f"split_{split_index}"), ann)]

        def _split_by_num() -> List[Tuple[ImageDescriptor, Annotation]]:
            split_num = self.settings["split_num"]
            split_index = int(item_idx / split_num) + (item_idx % split_num > 0)
            return [(replace_ds_name(f"split_{split_index}"), ann)]

        def _split_by_class() -> List[Tuple[ImageDescriptor, Annotation]]:
            image_labels = ann.labels
            if len(image_labels) == 0:
                return [(replace_ds_name("unlabeled"), ann)]
            classes = list({label.obj_class.name for label in image_labels})
            return [(replace_ds_name(class_name), ann) for class_name in classes]

        def _split_by_tags() -> List[Tuple[ImageDescriptor, Annotation]]:
            image_tags = list(set(ann.img_tags.keys()))
            label_tags = list({tag for label in ann.labels for tag in label.tags.keys()})
            all_tags_list = image_tags + label_tags
            if len(all_tags_list) == 0:
                return [(replace_ds_name("unlabeled"), ann)]

            tag_names = set()
            items = []
            for tag in all_tags_list:
                if tag not in tag_names:
                    tag_names.add(tag)
                    items.append((replace_ds_name(tag), ann))
            return items

        if self.net.preview_mode:
            yield data_el
        else:
            item_desc, ann = data_el
            item_idx = item_desc.get_item_idx()

            split_func_map = {
                "percent": _split_by_percent,
                "number": _split_by_num,
                "classes": _split_by_class,
                "tags": _split_by_tags,
            }
            split_method = self.settings["split_method"]
            func = split_func_map.get(split_method)
            items = func()
            yield from items

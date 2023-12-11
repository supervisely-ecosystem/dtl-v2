# coding: utf-8

from typing import List
import numpy as np

from supervisely import Bitmap, Label
from supervisely.sly_logger import logger

from src.exceptions import BadSettingsError, WrongGeometryError
from src.compute.Layer import Layer


class BitwiseMasksLayer(Layer):
    action = "bitwise_masks"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["type", "class_mask", "classes_to_correct"],
                "properties": {
                    "type": {"type": "string", "enum": ["or", "and", "nor"]},
                    "class_mask": {"type": "string"},
                    "classes_to_correct": {"type": "array", "items": {"type": "string"}},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def find_mask_labels(self, labels: List[Label], class_mask_name):
        mask_labels = []
        for label in labels:
            if label.obj_class.name == class_mask_name:
                if isinstance(label.geometry, Bitmap):
                    mask_labels.append(label)
        return mask_labels

    def bitwise_ops(self, type):
        ops = {
            "or": lambda m1, m2: np.logical_or(m1, m2),
            "and": lambda m1, m2: np.logical_and(m1, m2),
            "nor": lambda m1, m2: np.logical_xor(m1, m2),
        }
        if type not in ops:
            raise BadSettingsError(
                "Bitwise type <{}> not in list {}".format(type, list(ops.keys()))
            )
        return ops[type]

    def modifies_data(self):
        return True

    def process(self, data_el):
        img_desc, ann = data_el
        imsize = ann.img_size
        bitwise_type = self.settings["type"]
        class_mask_name = self.settings["class_mask"]

        mask_labels = self.find_mask_labels(ann.labels, class_mask_name)

        if len(mask_labels) == 0:
            extra = {
                "layer_config": self.config,
                "project_name": data_el[0].get_pr_name(),
                "ds_name": data_el[0].get_ds_name(),
                "image_name": data_el[0].get_item_name(),
            }
            logger.warn(
                "Image was skipped because mask labels not found",
                extra=extra,
            )
        for mask_label in mask_labels:
            target_origin, target_mask = mask_label.geometry.origin, mask_label.geometry.data
            full_target_mask = np.full(imsize, False, bool)

            full_target_mask[
                target_origin.row : target_origin.row + target_mask.shape[0],
                target_origin.col : target_origin.col + target_mask.shape[1],
            ] = target_mask

            new_labels = []

            for label in ann.labels:
                if (
                    label.obj_class.name not in self.settings["classes_to_correct"]
                    or label.obj_class.name == class_mask_name
                ):
                    new_labels.append(label)
                elif not isinstance(label.geometry, Bitmap):
                    new_labels.append(label)
                    logger.info(
                        f"Label {label.obj_class.name} has geometry {label.geometry.geometry_name} and will be skipped. Allowed only Bitmap geometry",
                        extra={
                            "layer_config": self.config,
                            "project_name": data_el[0].get_pr_name(),
                            "ds_name": data_el[0].get_ds_name(),
                            "image_name": data_el[0].get_item_name(),
                        },
                    )
                else:
                    origin, mask = label.geometry.origin, label.geometry.data
                    full_size_mask = np.full(imsize, False, bool)
                    full_size_mask[
                        origin.row : origin.row + mask.shape[0],
                        origin.col : origin.col + mask.shape[1],
                    ] = mask

                    func = self.bitwise_ops(bitwise_type)
                    new_mask = func(full_target_mask, full_size_mask).astype(bool)
                    if np.any(new_mask):
                        new_geometry = Bitmap(new_mask)
                        new_labels.append(Label(geometry=new_geometry, obj_class=label.obj_class))

            ann = ann.clone(labels=new_labels)

        yield img_desc, ann

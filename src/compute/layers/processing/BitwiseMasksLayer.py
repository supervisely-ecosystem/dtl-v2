# coding: utf-8

from typing import List
import numpy as np

from supervisely import Bitmap, Label

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

    def __init__(self, config):
        Layer.__init__(self, config)

    def find_mask_class(self, labels: List[Label], class_mask_name):
        for label in labels:
            if label.obj_class.name == class_mask_name:
                if not isinstance(label.geometry, Bitmap):
                    raise WrongGeometryError(
                        None,
                        "Bitmap",
                        label.geometry.geometry_name(),
                        extra={"layer": self.action},
                    )
                return label

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

    def process(self, data_el):
        img_desc, ann = data_el
        imsize = ann.img_size
        bitwise_type = self.settings["type"]
        class_mask_name = self.settings["class_mask"]

        mask_label = self.find_mask_class(ann.labels, class_mask_name)

        if mask_label is not None:
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
                else:
                    if not isinstance(label.geometry, Bitmap):
                        raise WrongGeometryError(
                            None,
                            "Bitmap",
                            label.geometry.geometry_name(),
                            extra={"layer": self.action},
                        )

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

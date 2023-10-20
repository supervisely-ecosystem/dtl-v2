# coding: utf-8

from typing import Tuple

from cv2 import connectedComponents
from supervisely import Annotation, Bitmap, Label

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels
from src.exceptions import WrongGeometryError


class SplitMasksLayer(Layer):
    action = "split_masks"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes"],
                "properties": {"classes": {"type": "array", "items": {"type": "string"}}},
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        def split_mask(label: Label):
            if label.obj_class.name not in self.settings["classes"]:
                return [label]

            if not isinstance(label.geometry, Bitmap):
                raise WrongGeometryError(
                    None,
                    "Bitmap",
                    label.geometry.geometry_name(),
                    extra={"layer": self.action},
                )

            old_origin, old_mask = label.geometry.origin, label.geometry.data
            ret, masks = connectedComponents(old_mask.astype("uint8"), connectivity=8)

            res_labels = []
            for i in range(1, ret):
                obj_mask = masks == i
                res_labels.append(label.clone(geometry=Bitmap(obj_mask, old_origin)))
            return res_labels

        ann = apply_to_labels(ann, split_mask)
        yield img_desc, ann

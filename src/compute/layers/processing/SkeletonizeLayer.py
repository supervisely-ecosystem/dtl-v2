# coding: utf-8

from typing import Tuple

import numpy as np
from skimage.morphology import skeletonize, medial_axis, thin
from exceptions import WrongGeometryError

from supervisely import Annotation, Label, Bitmap

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels


# processes FigureBitmap
class SkeletonizeLayer(Layer):
    action = "skeletonize"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes", "method"],
                "properties": {
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "method": {
                        "type": "string",
                        "enum": ["skeletonization", "medial_axis", "thinning"],
                    },
                },
            }
        },
    }

    method_mapping = {
        "skeletonization": skeletonize,
        "medial_axis": medial_axis,
        "thinning": thin,
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def define_classes_mapping(self):
        super().define_classes_mapping()  # don't change

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        method = self.method_mapping.get(self.settings["method"], None)
        if method is None:
            raise NotImplemented()

        def get_skel(label: Label):
            if label.obj_class.name not in self.settings["classes"]:
                return [label]
            if not isinstance(label.geometry, Bitmap):
                raise WrongGeometryError(
                    None,
                    "Bitmap",
                    label.geometry.geometry_name(),
                    extra={"layer": self.action},
                )

            origin, mask = label.geometry.origin, label.geometry.data
            mask_u8 = mask.astype(np.uint8)
            res_mask = method(mask_u8).astype(bool)
            new_geometry = Bitmap(res_mask, origin)
            new_label = label.clone(geometry=new_geometry)
            return [new_label]

        ann = apply_to_labels(ann, get_skel)
        yield img_desc, ann

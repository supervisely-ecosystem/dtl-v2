# coding: utf-8

from typing import Tuple
import numpy as np
from supervisely import Point, Annotation, Label, ObjClass

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class GenerateHintsLayer(Layer):
    action = "generate_hints"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["class", "positive_class", "negative_class", "min_points_number"],
                "properties": {
                    "class": {"type": "string"},
                    "positive_class": {"type": "string"},
                    "negative_class": {"type": "string"},
                    "min_points_number": {"type": "integer"},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)
        if self.settings["min_points_number"] < 0:
            raise ValueError("GenerateHintsLayer: min_points_number must not be less than zero")

    def define_classes_mapping(self):
        self.cls_mapping[ClassConstants.NEW] = [
            {"title": self.settings["positive_class"], "shape": Point.geometry_name()},
            {"title": self.settings["negative_class"], "shape": Point.geometry_name()},
        ]
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def generate_points(self, mask, color=1):
        h, w = mask.shape[:2]
        pos_area = mask.sum()

        def pt_num(cnt=2):
            cs = [
                int(np.random.exponential(2)) + self.settings["min_points_number"]
                for _ in range(cnt)
            ]
            return cs

        n_pos, n_neg = pt_num()
        n_pos = min(n_pos, pos_area)
        n_neg = min(n_neg, h * w - pos_area)
        positive_points, negative_points = [], []
        if n_pos > 0:
            # @TODO: speed up (np.argwhere, mm); what if pos or neg is missing?
            points = np.argwhere(mask == color)[:, [1, 0]]  # to xy
            positive_points = points[np.random.choice(points.shape[0], n_pos, replace=False), :]
        if n_neg > 0:
            points = np.argwhere(mask != color)[:, [1, 0]]  # to xy
            negative_points = points[np.random.choice(points.shape[0], n_neg, replace=False), :]
        return positive_points, negative_points

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        shape_hw = ann.img_size

        mask = np.zeros(shape_hw, dtype=np.uint8)

        for label in ann.labels:
            if label.obj_class.name == self.settings["class"]:
                label.draw(mask, 1)

        def add_pt_labels(ann: Annotation, pts, obj_class: ObjClass):
            for point in pts:
                new_geometry = Point(point[0], point[1])
                ann = ann.add_label(Label(new_geometry, obj_class))
            return ann

        positive_points, negative_points = self.generate_points(mask)
        positive_points_obj_class = ObjClass(self.settings["positive_class"], Point)
        negative_points_obj_class = ObjClass(self.settings["negative_class"], Point)
        ann = add_pt_labels(ann, positive_points, positive_points_obj_class)
        ann = add_pt_labels(ann, negative_points, negative_points_obj_class)

        yield img_desc, ann

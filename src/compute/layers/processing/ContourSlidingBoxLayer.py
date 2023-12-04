# coding: utf-8

from typing import List, Tuple
import math

from supervisely import Polygon, Rectangle, Annotation, Label, ObjClass
from supervisely.imaging.color import hex2rgb

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels
from src.exceptions import WrongGeometryError


def fix_coord(coord, min_value, max_value):
    return max(min_value, min(max_value, coord))


def simple_distance(p1, p2) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def normalize(p1, p2):
    x, y = p2[0] - p1[0], p2[1] - p1[1]
    norm = math.sqrt(x * x + y * y)
    if norm > 0:
        nx = x / norm
        ny = y / norm
    else:
        nx = ny = 0
    return nx, ny


def contour_stepper(lines, step=0.5, eps=0.1):
    path = 0.0
    counter = 0.0

    for point_index in range(1, len(lines)):
        previous_point = lines[point_index - 1]
        current_point = lines[point_index]

        vx, vy = normalize(previous_point, current_point)

        current_distance = simple_distance(previous_point, current_point)

        while path < current_distance:
            path = path + eps
            counter = counter + eps
            if counter >= step:
                counter = 0
                current_pos = [(previous_point[0] + vx * path), (previous_point[1] + vy * path)]
                yield current_pos

        path = path - current_distance


def generate_box(x, y, box_wh, image_wh):
    half_w = box_wh[0] // 2
    half_h = box_wh[1] // 2

    x = fix_coord(x, half_w, (image_wh[0] - 1) - half_w)
    y = fix_coord(y, half_h, (image_wh[1] - 1) - half_h)

    left = x - half_w
    right = x + half_w

    bottom = y + half_h
    top = y - half_h
    return left, top, right, bottom


def add_boxes_for_contour(label: Label, image_wh, box_wh, distance, box_class_title) -> List[Label]:
    labels = []

    figure_points = [[p.col, p.row] for p in label.geometry.exterior]
    figure_points.append(figure_points[0])

    for x, y in contour_stepper(figure_points, step=distance):
        left, top, right, bottom = generate_box(x, y, box_wh, image_wh)
        geometry = Rectangle(top, left, bottom, right)
        obj_class = ObjClass(
            name=box_class_title, geometry_type=Rectangle, color=hex2rgb("#00EE00")
        )
        rect_label = label.clone(geometry=geometry, obj_class=obj_class, tags=[], description="")
        labels.append(rect_label)

    return labels


class ContourSlidingBoxLayer(Layer):
    action = "contour_sliding_box"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["box", "distance", "classes", "box_class"],
                "properties": {
                    "box": {
                        "type": "object",
                        "uniqueItems": True,
                        "items": {
                            "type": "string",
                            "patternProperties": {
                                "(width)|(height)": {
                                    "type": "string",
                                    "pattern": "^[0-9]+(%)|(px)$",
                                }
                            },
                        },
                    },
                    "distance": {"type": "string", "pattern": "^[0-9]+(%)|(px)$"},
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "box_class": {"type": "string"},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def define_classes_mapping(self):
        new_class = self.settings["box_class"]
        self.cls_mapping[ClassConstants.NEW] = [
            {"title": new_class, "shape": Rectangle.geometry_name(), "color": "#00EE00"}
        ]
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def fix_percent(self, value, abs_value):
        if isinstance(value, str):
            if "%" in value:
                value = value.replace("%", "")
                if value.replace(".", "").isdigit():
                    return int(float(value) / 100.0 * abs_value)
            if "px" in value:
                value = value.replace("px", "")
                if value.isdigit():
                    return int(value)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        imsize_wh = ann.img_size[::-1]

        box_w = self.fix_percent(self.settings["box"]["width"], imsize_wh[0])
        box_h = self.fix_percent(self.settings["box"]["height"], imsize_wh[1])
        box_wh = [box_w, box_h]

        distance = self.fix_percent(self.settings["distance"], min(imsize_wh[0], imsize_wh[1]))

        classes = self.settings["classes"]
        box_class = self.settings["box_class"]

        def add_contour_boxies(label: Label):
            results = [label]
            if label.obj_class.name in classes:
                if not isinstance(label.geometry, Polygon):
                    raise WrongGeometryError(
                        None,
                        "Polygon",
                        label.geometry.geometry_name(),
                        extra={"layer": self.action},
                    )

                results.extend(
                    add_boxes_for_contour(
                        label,
                        image_wh=imsize_wh,
                        box_wh=box_wh,
                        distance=distance,
                        box_class_title=box_class,
                    )
                )
            return results

        ann = apply_to_labels(ann, add_contour_boxies)
        yield img_desc, ann

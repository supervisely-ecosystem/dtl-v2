# coding: utf-8

from typing import Tuple
import math

from supervisely import Polyline, Annotation, Label

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels


def distance(p1, p2) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_line_path(line: list) -> float:
    path = 0.0
    for i in range(1, len(line)):
        path += distance(line[i - 1], line[i])
    return path


def check_line_by_length(line: Polyline, min_length, max_length, invert):
    points = line.exterior_np
    line_length = get_line_path(points)

    result = True
    if min_length is not None:
        result = result and (line_length >= min_length)
    if max_length is not None:
        result = result and (line_length <= max_length)

    if invert is True:
        result = not result
    return result


class DropLinesByLengthLayer(Layer):
    action = "drop_lines_by_length"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["lines_class"],
                "properties": {
                    "lines_class": {
                        "description_en": "Class-name of lines for processing",
                        "description_ru": "Название класса линий для обработки",
                        "type": "string",
                        "minLength": 1,
                    },
                    "min_length": {
                        "description_en": "Mininal length for no-deleted line candidate",
                        "description_ru": "Минимальная длина линии, которая не будет удалена",
                        "type": "number",
                        "minimum": 0,
                    },
                    "max_length": {
                        "description_en": "Maximal length for no-deleted line candidate",
                        "description_ru": "Максимальная длина линии, которая не будет удалена",
                        "type": "number",
                        "minimum": 0,
                    },
                    "invert": {
                        "description_en": "Invert remove decisions for lines",
                        "description_ru": "Обратить результаты отбора линий",
                        "type": "boolean",
                    },
                    "resolution_compensation": {
                        "description_en": "Length compensation for different resolutions",
                        "description_ru": "Компенсация длины линий при разных разрешениях",
                        "type": "boolean",
                    },
                },
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        imgsize_hw = ann.img_size

        lines_class = self.settings.get("lines_class")
        min_length = self.settings.get("min_length", None)
        max_length = self.settings.get("max_length", None)
        invert_opt = self.settings.get("invert", False)
        resolution_compensation = self.settings.get("resolution_compensation", False)

        if (min_length is None) and (max_length is None):
            raise RuntimeError(
                self,
                '"min_length" and/or "max_length" properties should be selected for "delete_lines_by_length" layer',
            )

        if resolution_compensation:
            compensator = imgsize_hw[1] / 1000.0
            if min_length is not None:
                min_length *= compensator
            if max_length is not None:
                max_length *= compensator

        def drop_by_line_length(label: Label):
            if not isinstance(label.geometry, Polyline):
                return [label]
            if lines_class == label.obj_class.name:
                if check_line_by_length(label.geometry, min_length, max_length, invert_opt):
                    return [label]
                else:
                    return []
            else:
                return [label]

        ann = apply_to_labels(ann, drop_by_line_length)
        yield img_desc, ann

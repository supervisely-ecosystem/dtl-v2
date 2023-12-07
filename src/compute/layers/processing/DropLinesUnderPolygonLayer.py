# coding: utf-8

from typing import List, Tuple
import numpy as np

from supervisely import Polyline, Polygon, Annotation, Label

from src.compute.Layer import Layer
from shapely.geometry import LineString, Polygon as shPolygon
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels


def remove_polylines_inside_polygon(line: Polyline, polygons: List[Polygon]) -> List[Polyline]:
    coords = line.exterior_np
    sh_line = LineString(coords)

    sh_polygons = []
    for polygon in polygons:
        c_exterior = polygon.exterior_np
        c_interiors = polygon.interior_np
        poly = shPolygon(shell=c_exterior, holes=c_interiors)
        if poly.is_valid == False:
            poly = poly.buffer(0.001)

        sh_polygons.append(poly)

    for poly in sh_polygons:
        sh_line = sh_line.difference(poly)

    # ?
    if sh_line.geom_type == "GeometryCollection" or sh_line.is_empty:
        return []

    if sh_line.geom_type == "MultiLineString":
        new_lines = []
        for line in sh_line:
            coords = np.transpose(line.coords.xy)
            new_lines.append(Polyline([(c[0], c[1]) for c in coords]))
        return new_lines

    if sh_line.geom_type == "LineString":
        coords = np.transpose(sh_line.coords.xy)
        return [Polyline([(c[0], c[1]) for c in coords])]


class DropLinesUnderPolygonLayer(Layer):
    action = "drop_lines_under_polygon"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["lines_class", "polygons_class"],
                "properties": {
                    "lines_class": {"type": "string", "minLength": 1},
                    "polygons_class": {"type": "string", "minLength": 1},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el

        lines_class = self.settings.get("lines_class")
        polygons_class = self.settings.get("polygons_class")

        polygons = []
        for label in ann.labels:
            if polygons_class == label.obj_class.name and isinstance(label.geometry, Polygon):
                polygons.append(label.geometry)

        def drop_lines(label: Label):
            if lines_class != label.obj_class.name or not isinstance(label.geometry, Polyline):
                return [label]
            new_lines = remove_polylines_inside_polygon(label.geometry, polygons)
            return [label.clone(geometry=line) for line in new_lines]

        ann = apply_to_labels(ann, drop_lines)
        yield img_desc, ann

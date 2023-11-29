# coding: utf-8

from copy import deepcopy
from typing import Tuple, Union

from supervisely import Annotation, Polygon, Rectangle, Label, VideoAnnotation
from supervisely.geometry.helpers import geometry_to_polygon

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor, VideoDescriptor
from src.compute.dtl_utils import apply_to_labels, convert_video_annotation
from src.exceptions import WrongGeometryError


class BBoxToPolyLayer(Layer):
    action = "bbox2poly"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_mapping"],
                "properties": {
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    }
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_mapping"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Polygon.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(
        self,
        data_el: Tuple[Union[ImageDescriptor, VideoDescriptor], Union[Annotation, VideoAnnotation]],
    ):
        item_desc, ann = data_el

        def to_geom_rect(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name)
            if new_title is None:
                return [label]
            if not isinstance(label.geometry, Rectangle):
                raise WrongGeometryError(
                    None,
                    "Rectangle",
                    label.geometry.geometry_name(),
                    extra={"layer": self.action},
                )

            poly = geometry_to_polygon(label.geometry)[0]
            result_obj_class = label.obj_class.clone(name=new_title, geometry_type=Polygon)
            result_label = label.clone(geometry=poly, obj_class=result_obj_class)
            return [result_label]  # iterable

        if isinstance(ann, Annotation):
            ann = apply_to_labels(ann, to_geom_rect)
        else:
            ann = convert_video_annotation(ann, self.output_meta)
        yield item_desc, ann

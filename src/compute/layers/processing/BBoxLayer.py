# coding: utf-8

from typing import Tuple, Union
from supervisely import Rectangle, Label, Annotation, VideoAnnotation

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils import apply_to_labels, convert_video_annotation
from src.compute.dtl_utils.item_descriptor import ImageDescriptor, VideoDescriptor


class BBoxLayer(Layer):
    action = "bbox"

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
            self.cls_mapping[old_class] = {"title": new_class, "shape": Rectangle.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(
        self,
        data_el: Tuple[Union[ImageDescriptor, VideoDescriptor], Union[Annotation, VideoAnnotation]],
    ):
        item_desc, ann = data_el

        def to_fig_rect(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name)
            if new_title is None:
                return [label]
            rect = label.geometry.to_bbox()
            new_obj_class = label.obj_class.clone(
                name=new_title, geometry_type=Rectangle
            )  # keep color?
            label = label.clone(
                geometry=rect, obj_class=new_obj_class
            )  # keep description and binding key?
            return [label]  # iterable

        if isinstance(ann, Annotation):
            ann = apply_to_labels(ann, to_fig_rect)
        else:
            ann = convert_video_annotation(ann, self.output_meta)
        yield item_desc, ann

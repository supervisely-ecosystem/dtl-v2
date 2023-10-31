# coding: utf-8
from typing import Tuple

from supervisely import Annotation, Label, Rectangle, ObjClass

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class BackgroundLayer(Layer):
    action = "background"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["class"],
                "properties": {"class": {"type": "string"}},
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)
        self.src_check_mappings = [self.settings["class"]]

    def define_classes_mapping(self):
        self.cls_mapping[ClassConstants.NEW] = [
            {"title": self.settings["class"], "shape": Rectangle.geometry_name()}
        ]
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        h, w = ann.img_size

        bg_label = Label(
            geometry=Rectangle(0, 0, h - 1, w - 1),
            obj_class=ObjClass(self.settings["class"], Rectangle),
        )

        ann = ann.add_label(bg_label)

        yield img_desc, ann

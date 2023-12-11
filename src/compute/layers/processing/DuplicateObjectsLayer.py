# coding: utf-8

from typing import Tuple

from supervisely import Annotation, Label

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels
from src.exceptions import BadSettingsError


class DuplicateObjectsLayer(Layer):
    action = "duplicate_objects"

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
        self.cls_mapping[ClassConstants.CLONE] = self.settings["classes_mapping"]
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.CLONE
        # self.cls_mapping[ClassConstants.OTHER] = ClassConstants.IGNORE

    def class_mapper(self, label: Label):
        curr_class = label.obj_class.name

        if curr_class in self.settings["classes_mapping"]:
            new_class = self.settings["classes_mapping"][curr_class]
        elif curr_class in self.cls_mapping:
            new_class = self.cls_mapping[curr_class]
        else:
            raise BadSettingsError("Can not find mapping for class", extra={"class": curr_class})

        if new_class == ClassConstants.IGNORE or new_class == ClassConstants.CLONE:
            return [label]  # don't change
        elif new_class == ClassConstants.DEFAULT:
            return [label, label]  # copy object
        else:
            new_obj_class = label.obj_class.clone(name=new_class)
            duplicate = label.clone(obj_class=new_obj_class)
            return [label, duplicate]

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        ann = apply_to_labels(ann, self.class_mapper)
        yield img_desc, ann

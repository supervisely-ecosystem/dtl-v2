# coding: utf-8

from typing import Tuple

from supervisely import Annotation
from supervisely.aug.aug import instance_crop

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class InstancesCropLayer(Layer):
    action = "instances_crop"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes", "pad"],
                "properties": {
                    "classes": {"type": "array", "items": {"type": "string"}},
                    "save_classes": {"type": "array", "items": {"type": "string"}},
                    "pad": {
                        "type": "object",
                        "required": ["sides"],
                        "properties": {
                            "sides": {
                                "type": "object",
                                "uniqueItems": True,
                                "items": {
                                    "type": "string",
                                    "patternProperties": {
                                        "(left)|(top)|(bottom)|(right)": {
                                            "type": "string",
                                            "pattern": "^[0-9]+(%)|(px)$",
                                        }
                                    },
                                },
                            }
                        },
                    },
                },
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)
        self.classes_to_crop, self.classes_to_save = self._get_cls_lists()

    def validate(self):
        super().validate()
        if len(self.classes_to_crop) == 0:
            raise ValueError("InstancesCropLayer: classes array can not be empty")
        if len(set(self.classes_to_crop) & set(self.classes_to_save)) > 0:
            raise ValueError("InstancesCropLayer: classes and save_classes must not intersect")

    def _get_cls_lists(self):
        return self.settings["classes"], self.settings.get("save_classes", [])

    def requires_image(self):
        return True

    def define_classes_mapping(self):
        classes_to_crop, classes_to_save = self._get_cls_lists()
        for cls in classes_to_save + classes_to_crop:
            self.cls_mapping[cls] = ClassConstants.DEFAULT
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.IGNORE

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        padding_dct = self.settings["pad"]["sides"]

        for obj_class_name in self.classes_to_crop:
            results = instance_crop(
                img=img_desc.read_image(),
                ann=ann,
                class_title=obj_class_name,
                save_other_classes_in_crop=False,
                padding_config=padding_dct,
            )

            for idx, (new_img, new_ann) in enumerate(results):
                new_img_desc = img_desc.clone_with_img(new_img).clone_with_name(
                    img_desc.get_img_name() + "_crop_" + obj_class_name + str(idx)
                )
                new_img_desc = new_img_desc
                yield new_img_desc, new_ann

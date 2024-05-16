# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Label, Bitmap, Polygon, Rectangle
from src.compute.classes_utils import ClassConstants
from imgaug import augmenters as iaa
from src.compute.dtl_utils import apply_to_labels
from src.exceptions import BadSettingsError


class PerspectiveTransformLayer(Layer):
    action = "perspective_transform"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["scale", "classes_mapping", "size_box"],
                "properties": {
                    "scale": {
                        "type": "object",
                        "required": ["min", "max"],
                        "properties": {
                            "min": {"type": "number", "minimum": 0.01, "maximum": 0.5},
                            "max": {"type": "number", "minimum": 0.01, "maximum": 0.5},
                        },
                    },
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    },
                    "size_box": {
                        "type": "object",
                        "required": ["keep", "fit"],
                        "properties": {"keep": {"type": "boolean"}, "fit": {"type": "boolean"}},
                    },
                    "cval": {
                        "type": "object",
                        "required": ["value"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 255},
                        },
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        self._res_meta = None
        Layer.__init__(self, config, net=net)

    def validate(self):
        super().validate()

        def check_min_max(dictionary, text):
            if dictionary["min"] > dictionary["max"]:
                raise BadSettingsError('"min" should be <= than "max" for "{}"'.format(text))

        check_min_max(self.settings["scale"], "scale")

    def modifies_data(self):
        return False

    def requires_item(self):
        return True

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_mapping"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Bitmap.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        from supervisely.aug.imgaug_utils import apply as apply_augs

        img_desc, ann = data_el
        img = img_desc.read_image()

        scale_value = self.settings["scale"]
        keep = self.settings["size_box"]["keep"]
        fit = self.settings["size_box"]["fit"]
        cval = self.settings["cval"]["value"]

        scale = (scale_value["min"], scale_value["max"])

        aug = iaa.Sequential(
            [iaa.PerspectiveTransform(scale=scale, cval=cval, keep_size=keep, fit_output=fit)]
        )  # todo checkbox

        def to_bitmap(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name, None)
            if new_title is None:
                return [label]
            new_obj_class = label.obj_class.clone(name=new_title, geometry_type=Bitmap)
            return label.convert(new_obj_class)

        ann = apply_to_labels(ann, to_bitmap)
        shapes_to_ignore = [Bitmap, Polygon, Rectangle]
        labels_to_add = [
            label for label in ann.labels if label.obj_class.geometry_type not in shapes_to_ignore
        ]

        _, res_img, res_ann = apply_augs(aug, self.output_meta, img, ann, "instance")
        res_ann = res_ann.add_labels(labels_to_add)
        new_img_desc = img_desc.clone_with_item(res_img)
        yield (new_img_desc, res_ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

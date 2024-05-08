# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Label, Bitmap
from src.compute.classes_utils import ClassConstants
from imgaug import augmenters as iaa
from src.compute.dtl_utils import apply_to_labels


class ElasticTransformationLayer(Layer):
    action = "elastic_transformation"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["alpha", "sigma", "classes_mapping"],
                "properties": {
                    "alpha": {"type": "integer"},
                    "sigma": {"type": "integer"},
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        self._res_meta = None
        Layer.__init__(self, config, net=net)

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

        alpha = self.settings["alpha"]
        sigma = self.settings["sigma"]
        aug = iaa.Sequential([iaa.ElasticTransformation(alpha=alpha, sigma=sigma)])

        def to_bitmap(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name, None)
            if new_title is None:
                return [label]
            new_obj_class = label.obj_class.clone(name=new_title, geometry_type=Bitmap)
            return label.convert(new_obj_class)

        ann = apply_to_labels(ann, to_bitmap)

        _, res_img, res_ann = apply_augs(aug, self.output_meta, img, ann)
        new_img_desc = img_desc.clone_with_item(res_img)
        yield (new_img_desc, res_ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

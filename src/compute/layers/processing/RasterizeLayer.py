# coding: utf-8

from typing import Tuple
import numpy as np
from supervisely import Bitmap, Annotation, Label, ObjClass, ProjectMeta

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor


def convert_to_nonoverlapping(src_ann: Annotation, project_meta: ProjectMeta, classes_mapping: dict) -> Annotation:
    new_labels = []
    # rasterized_labels = []
    # non_rasterized_labels = []
    common_img = np.zeros(src_ann.img_size, np.int32)
    for idx, lbl in enumerate(src_ann.labels, start=1):
        if lbl.obj_class.name in classes_mapping:
            lbl.draw(common_img, color=idx)
        else:
            new_labels.append(lbl)
            # non_rasterized_labels.append(lbl)

    for idx, lbl in enumerate(src_ann.labels, start=1):
        new_cls = project_meta.obj_classes.get(lbl.obj_class.name)
        new_lbls = lbl.convert(new_cls)
        mask = common_img == idx
        if np.any(mask):
            g = lbl.geometry
            new_bmp = Bitmap(
                data=mask,           
                labeler_login=g.labeler_login,
                updated_at=g.updated_at,
                created_at=g.created_at
            )
            for lbl in new_lbls:
                new_lbl = lbl.clone(geometry=new_bmp, obj_class=new_cls).to_json()
                new_lbl = Label.from_json(new_lbl, project_meta)
                new_labels.append(new_lbl)
                # rasterized_labels.append(new_lbl)
    # new_labels = rasterized_labels + non_rasterized_labels
    return src_ann.clone(labels=new_labels)

# converts ALL types to FigureBitmap
class RasterizeLayer(Layer):
    action = "rasterize"

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
            self.cls_mapping[old_class] = {"title": new_class, "shape": Bitmap.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def modifies_data(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        ann = convert_to_nonoverlapping(ann, self.output_meta, self.settings["classes_mapping"])
        yield img_desc, ann

# coding: utf-8
import json
import os.path as osp
from typing import Tuple

import cv2
import numpy as np

import supervisely as sly
from supervisely.project.project import Dataset

from src.compute.utils import imaging
from src.compute.utils import os_utils
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from src.exceptions import GraphError


# save to archive
class SaveLayer(Layer):
    action = "save"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "properties": {
                    "images": {"type": "boolean"},  # Deprecated
                    "annotations": {"type": "boolean"},  # Deprecated
                    "visualize": {"type": "boolean"},
                },
            }
        },
    }

    @classmethod
    def draw_colored_mask(cls, ann: sly.Annotation, color_mapping):
        h, w = ann.img_size
        line_w = int((max(w, h) + 1) / 300)
        line_w = max(line_w, 1)
        res_img = np.zeros((h, w, 3), dtype=np.uint8)

        for label in ann.labels:
            color = color_mapping.get(label.obj_class.name)
            if color is None:
                continue
            if isinstance(label.geometry, sly.Bitmap) or isinstance(label.geometry, sly.Polygon):
                label.geometry.draw(res_img, color)
            else:
                label.geometry.draw_contour(res_img, color, line_w)

        return res_img

    def __init__(self, config, output_folder, net):
        Layer.__init__(self, config)
        self.output_folder = output_folder
        self.net = net

    def is_archive(self):
        return True

    def requires_image(self):
        return True

    def validate_dest_connections(self):
        pass

    def preprocess(self):
        if self.net.preview_mode:
            return
        if self.output_meta is None:
            raise GraphError(
                "Output meta is not set. Check that node is connected", extra={"layer": self.action}
            )
        dst = self.dsts[0]
        self.out_project = sly.Project(
            directory=f"{self.output_folder}/{dst}", mode=sly.OpenMode.CREATE
        )
        with open(self.out_project.directory + "/meta.json", "w") as f:
            json.dump(self.output_meta.to_json(), f)

        # Deprecate warning
        for param in ["images", "annotations"]:
            if param in self.settings:
                sly.logger.warning(
                    "'save' layer: '{}' parameter is deprecated. Skipped.".format(param)
                )

    def process(self, data_el: Tuple[ImageDescriptor, sly.Annotation]):
        img_desc, ann = data_el

        if not self.net.preview_mode:
            free_name = self.net.get_free_name(img_desc, self.out_project.name)
            new_dataset_name = img_desc.get_res_ds_name()

            if self.settings.get("visualize"):
                out_meta = self.output_meta
                out_meta: sly.ProjectMeta
                cls_mapping = {}
                for obj_class in out_meta.obj_classes:
                    color = obj_class.color
                    if color is None:
                        color = sly.color.random_rgb()
                    cls_mapping[obj_class.name] = color

                # hack to draw 'black' regions
                cls_mapping = {k: (1, 1, 1) if max(v) == 0 else v for k, v in cls_mapping.items()}

                vis_img = self.draw_colored_mask(ann, cls_mapping)
                orig_img = img_desc.read_image()
                comb_img = imaging.overlay_images(orig_img, vis_img, 0.5)

                sep = np.array([[[0, 255, 0]]] * orig_img.shape[0], dtype=np.uint8)
                img = np.hstack((orig_img, sep, comb_img))

                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                output_img_path = osp.join(
                    self.output_folder,
                    self.out_project.name,
                    new_dataset_name,
                    "visualize",
                    free_name + ".png",
                )
                os_utils.ensure_base_path(output_img_path)
                cv2.imwrite(output_img_path, img)

            dataset_name = img_desc.get_res_ds_name()
            if not self.out_project.datasets.has_key(dataset_name):
                self.out_project.create_dataset(dataset_name)
            out_dataset = self.out_project.datasets.get(dataset_name)

            out_item_name = free_name + img_desc.get_image_ext()

            # net _always_ downloads images
            if img_desc.need_write():
                out_dataset: Dataset
                out_dataset.add_item_np(out_item_name, img_desc.image_data, ann=ann)
            else:
                out_dataset.add_item_file(out_item_name, img_desc.get_img_path(), ann=ann)

        yield ([img_desc, ann],)

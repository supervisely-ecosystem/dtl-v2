# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Bitmap, Rectangle, Polygon, Label
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug.augmentables.polys import PolygonsOnImage
from imgaug.augmentables.polys import Polygon as iaaPolygon
import numpy as np


def augment_boxes(aug: iaa.ElasticTransformation, labels: List[Label], img_size: Tuple[int, int]):
    boxes = [label.geometry.to_bbox() for label in labels]
    ia_boxes = [BoundingBox(box.left, box.top, box.right, box.bottom) for box in boxes]
    imgaug_boxes = BoundingBoxesOnImage(ia_boxes, img_size)
    augmented_boxes = aug.augment_bounding_boxes(imgaug_boxes)
    # augmented_boxes = augmented_boxes.items()
    for label, box in zip(labels, augmented_boxes):
        new_label = label.clone(
            geometry=Rectangle(
                box.x2_int,
                box.y2_int,
                box.x1_int,
                box.y1_int,
            )
        )
        yield new_label


def augment_masks(aug: iaa.ElasticTransformation, labels: List[Label]):
    masks = [label.geometry.data for label in labels]
    augmented_masks = aug.augment_images(masks)
    for label, mask in zip(labels, augmented_masks):
        new_label = label.clone(geometry=Bitmap(data=mask))
        yield new_label


def augment_polygons(
    aug: iaa.ElasticTransformation, labels: List[Label], img_size: Tuple[int, int]
):
    numpy_to_tuples = lambda polygon_array: [tuple(map(float, point)) for point in polygon_array]
    ext_np = [label.geometry.exterior_np for label in labels]
    ext_iaa = PolygonsOnImage([iaaPolygon(p) for p in ext_np], shape=img_size)
    aug_ext = aug.augment_polygons(ext_iaa)

    int_np = [label.geometry.interior_np for label in labels]
    # int_np = [points if len(points) > 0 else None for points in int_np]
    aug_int = [None]
    if len(int_np[0]) != 0:
        int_iaa = PolygonsOnImage([iaaPolygon(p) for p in int_np], shape=img_size)
        aug_int = aug.augment_polygons(int_iaa)

    for label, aug_ex, aug_int in zip(labels, aug_ext, aug_int):
        aug_ex = aug_ex.exterior
        aug_int = aug_int.exterior if aug_int is not None else []
        new_label = label.clone(geometry=Polygon(numpy_to_tuples(aug_ex), aug_int))  # todo interior
        yield new_label


class ElasticTransformLayer(Layer):
    action = "elastic_transform"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["alpha", "sigma"],
                "properties": {"alpha": {"type": "integer"}, "sigma": {"type": "integer"}},
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def modifies_data(self):
        return False

    def requires_item(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img = img_desc.read_image()

        alpha = self.settings["alpha"]
        sigma = self.settings["sigma"]
        aug = iaa.ElasticTransformation(alpha, sigma)
        img_size = img.shape

        processed_img = aug.augment_image(img.astype(np.uint8))
        new_img_desc = img_desc.clone_with_item(processed_img)

        boxes_labels = [label for label in ann.labels if label.obj_class.geometry_type == Rectangle]
        masks_labels = [label for label in ann.labels if label.obj_class.geometry_type == Bitmap]
        polygon_labels = [label for label in ann.labels if label.obj_class.geometry_type == Polygon]
        other_labels = [
            label
            for label in ann.labels
            if (label.obj_class.geometry_type != Rectangle)
            and (label.obj_class.geometry_type != Bitmap)
            and (label.obj_class.geometry_type != Polygon)
        ]

        new_labels = []
        if polygon_labels:
            for label in augment_polygons(aug, polygon_labels, img_size):  # todo check
                new_labels.append(label)
        if masks_labels:
            for label in augment_masks(aug, masks_labels):
                new_labels.append(label)
        if boxes_labels:
            for label in augment_boxes(aug, boxes_labels, img_size):
                new_labels.append(label)
        if len(other_labels) > 0:
            new_labels.extend(other_labels)

        new_ann = ann.clone(labels=new_labels)

        yield (new_img_desc, new_ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

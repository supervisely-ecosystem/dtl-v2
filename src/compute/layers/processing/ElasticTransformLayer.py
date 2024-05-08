# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Bitmap, Rectangle, Polygon, Label, ProjectMeta, ObjClass
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


def compare_project_metas(meta1, meta2):
    # Dictionaries to store class names and their geometries
    classes1 = {obj_class.name: obj_class.geometry_type for obj_class in meta1.obj_classes}
    classes2 = {obj_class.name: obj_class.geometry_type for obj_class in meta2.obj_classes}

    # Set to store classes with the same name but different geometries
    differing_classes = {}

    # Compare object classes from both metas
    for class_name, geometry1 in classes1.items():
        geometry2 = classes2.get(class_name)
        if geometry2 and geometry1 != geometry2:
            differing_classes[class_name] = (geometry1, geometry2)

    return differing_classes


def process_annotations(ann1: Annotation, ann2: Annotation, meta1, meta2):
    differing_classes = compare_project_metas(meta1, meta2)

    new_labels = []
    for label in ann1.labels + ann2.labels:
        class_name = label.obj_class.name
        if class_name in differing_classes:
            original_geometry = differing_classes[class_name][0]
            if original_geometry == Polygon:
                label.clone()
                contours = label.geometry.to_contours()
                label_list = [label.clone(geometry=contour) for contour in contours]
                new_labels.extend(label_list)
        else:
            new_labels.append(label)

    new_ann = ann1.clone(labels=new_labels)

    return new_ann


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

    # def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
    #     img_desc, ann = data_el
    #     img = img_desc.read_image()

    #     alpha = self.settings["alpha"]
    #     sigma = self.settings["sigma"]
    #     aug = iaa.Sequential([iaa.ElasticTransformation(alpha=alpha, sigma=sigma)])

    #     processed_img = aug.augment_image(img.astype(np.uint8))
    #     new_img_desc = img_desc.clone_with_item(processed_img)

    #     boxes_labels = [label for label in ann.labels if label.obj_class.geometry_type == Rectangle]
    #     masks_labels = [label for label in ann.labels if label.obj_class.geometry_type == Bitmap]
    #     polygon_labels = [label for label in ann.labels if label.obj_class.geometry_type == Polygon]
    #     other_labels = [
    #         label
    #         for label in ann.labels
    #         if (label.obj_class.geometry_type != Rectangle)
    #         and (label.obj_class.geometry_type != Bitmap)
    #         and (label.obj_class.geometry_type != Polygon)
    #     ]

    #     new_labels = []
    #     if polygon_labels:
    #         for label in augment_polygons(aug, polygon_labels, img.shape):
    #             new_labels.append(label)
    #     if masks_labels:
    #         for label in augment_masks(aug, masks_labels):
    #             new_labels.append(label)
    #     if boxes_labels:
    #         for label in augment_boxes(aug, boxes_labels, img.shape):
    #             new_labels.append(label)
    #     if len(other_labels) > 0:
    #         new_labels.extend(other_labels)

    #     new_ann = ann.clone(labels=new_labels)

    #     yield (new_img_desc, new_ann)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        from supervisely.aug.imgaug_utils import apply as apply_augs

        img_desc, ann = data_el
        img = img_desc.read_image()

        alpha = self.settings["alpha"]
        sigma = self.settings["sigma"]
        aug = iaa.Sequential([iaa.ElasticTransformation(alpha=alpha, sigma=sigma)])

        res_meta, res_img, res_ann = apply_augs(aug, self.output_meta, img, ann)
        new_img_desc = img_desc.clone_with_item(res_img)

        # new_ann = process_annotations(ann, res_ann, self.output_meta, res_meta)

        yield (new_img_desc, res_ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

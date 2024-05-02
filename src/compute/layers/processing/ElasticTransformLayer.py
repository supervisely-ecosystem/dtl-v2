# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, Bitmap, Rectangle, Polygon, Label
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
from imgaug.augmentables.segmaps import SegmentationMapsOnImage
from numpy import ndarray


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

    def augment_boxes(
        aug: iaa.ElasticTransformation, labels: List[Label], img_size: Tuple[int, int]
    ):
        boxes = [label.geometry.to_bbox() for label in labels]
        ia_boxes = [BoundingBox(box.left, box.top, box.right, box.bottom) for box in boxes]
        imgaug_boxes = BoundingBoxesOnImage(ia_boxes, img_size)
        augmented_boxes = aug.augment_bounding_boxes(imgaug_boxes)
        augmented_boxes = augmented_boxes.items()
        for label, box in zip(labels, augmented_boxes):
            label.geometry = Rectangle(
                box.x2_int,
                box.y2_int,
                box.x1_int,
                box.y1_int,
                label.geometry.sly_id,
                label.geometry.class_id,
            )

    def augment_masks(aug: iaa.ElasticTransformation, labels: List[Label]):
        masks = [label.geometry.data for label in labels]
        augmented_masks = aug.augment_images(masks)
        for label, mask in zip(labels, augmented_masks):
            label.geometry.data = mask

    def augment_polygons(
        aug: iaa.ElasticTransformation, labels: List[Label], img_size: Tuple[int, int]
    ):
        ext_np = [label.geometry.exterior_np for label in labels]
        int_np = [label.geometry.interior_np for label in labels]

        aug_ext_np = [
            aug.augment_segmentation_maps(SegmentationMapsOnImage(arr, img_size)) for arr in ext_np
        ]
        aug_int_np = [
            aug.augment_segmentation_maps(SegmentationMapsOnImage(arr, img_size)) for arr in int_np
        ]
        aug_points_list = []
        for ext, int in zip(aug_ext_np, aug_int_np):
            aug_ext_np = [segmap.get_arr() for segmap in ext]
            aug_int_np = [segmap.get_arr() for segmap in int]

            aug_ext = aug_ext_np.tolist()
            aug_int = aug_int_np.tolist()
            aug_points_list.append((aug_ext, aug_int))

        for label, points in zip(labels, aug_points_list):
            exterior, interior = points
            label.geometry = Polygon(
                exterior, interior, label.geometry.sly_id, label.geometry.class_id
            )

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        # if img_desc.item_data is None:

        alpha = self.settings["alpha"]
        sigma = self.settings["sigma"]
        aug = iaa.ElasticTransformation(alpha, sigma)
        img_size = (img_desc.info.item_info.width, img_desc.info.item_info.height)
        # print(img_size)

        processed_img = aug.augment_image(img_desc.item_data)
        img_desc.update_item(processed_img)

        boxes_labels = [label for label in ann.labels if label.obj_class.geometry_type == Rectangle]
        self.augment_boxes(aug, boxes_labels, img_size) if boxes_labels else None

        masks_labels = [label for label in ann.labels if label.obj_class.geometry_type == Bitmap]
        self.augment_masks(aug, masks_labels) if masks_labels else None

        polygon_labels = [label for label in ann.labels if label.obj_class.geometry_type == Polygon]
        self.augment_polygons(aug, polygon_labels, img_size) if polygon_labels else None
        yield (img_desc, ann)

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        item_descs, anns = zip(*data_els)
        yield tuple(zip(item_descs, anns))

    def has_batch_processing(self) -> bool:
        return False

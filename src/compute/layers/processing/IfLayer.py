# coding: utf-8

from typing import Tuple
import random
import re

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.exceptions import BadSettingsError


class IfLayer(Layer):
    action = "if"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "dst": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "string"}},
            "settings": {
                "type": "object",
                "required": ["condition"],
                "properties": {
                    "condition": {
                        "maxItems": 1,
                        "oneOf": [
                            {
                                "type": "object",
                                "required": ["probability"],
                                "properties": {
                                    "probability": {"type": "number", "minimum": 0, "maximum": 1}
                                },
                            },
                            {
                                "type": "object",
                                "required": ["regex_names"],
                                "properties": {
                                    "regex_names": {"type": "array", "items": {"type": "string"}}
                                },
                            },
                            {
                                "type": "object",
                                "required": ["project_datasets"],
                                "properties": {
                                    "project_datasets": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                },
                            },
                            {
                                "type": "object",
                                "required": ["min_objects_count"],
                                "properties": {
                                    "min_objects_count": {"type": "integer", "minimum": 0}
                                    # comparator is greater or equal
                                },
                            },
                            {
                                "type": "object",
                                "required": ["include_classes"],
                                "properties": {
                                    "include_classes": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    }
                                },
                            },
                            {
                                "type": "object",
                                "required": ["tags"],
                                "properties": {
                                    "tags": {"type": "array", "items": {"type": "string"}}
                                },
                            },
                            {
                                "type": "object",
                                "required": ["min_height"],
                                "properties": {"min_height": {"type": "integer"}},
                            },
                            {
                                "type": "object",
                                "required": ["min_width"],
                                "properties": {"min_width": {"type": "integer"}},
                            },
                            {
                                "type": "object",
                                "required": ["min_area"],
                                "properties": {"min_area": {"type": "integer"}},
                            },
                            {
                                "type": "object",
                                "required": ["sum_object_area", "classes"],
                                "properties": {
                                    "sum_object_area": {"type": "number"},
                                    "classes": {"type": "array", "items": {"type": "string"}},
                                },
                            },  # comparator is greater or equal
                            {
                                "type": "object",
                                "required": ["name_in_range", "frame_step"],
                                "properties": {
                                    "name_in_range": {
                                        "type": "array",
                                        "minItems": 2,
                                        "maxItems": 2,
                                        "items": {"type": "string"},
                                    },
                                    "frame_step": {"type": "integer"},
                                },
                            },
                        ],
                    }
                },
            },
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

        self.frame_counter = 0

    # for compatibility; format "project/dataset"
    @classmethod
    def _check_project_dataset_str(cls, s):
        src_regex = r"^[^/]+/[^/]+$"
        if not re.search(src_regex, s):
            raise BadSettingsError(
                'Project/dataset string "{}" does not match regex "{}"'.format(s, src_regex)
            )

    @classmethod
    def _matches_ast(cls, pattern, s):
        res = (pattern == "*") or (pattern == s)
        return res

    @classmethod
    def _pr_ds_matches(cls, project_dataset_str, img_desc):
        splitted = project_dataset_str.split("/")
        if len(splitted) != 2:
            raise BadSettingsError('Wrong project_dataset string "{}"'.format(project_dataset_str))
        pr_name, ds_name = splitted
        res = cls._matches_ast(pr_name, img_desc.get_pr_name()) and cls._matches_ast(
            ds_name, img_desc.get_ds_name()
        )
        return res

    @classmethod
    def is_image_name_in_range(cls, img_name, min_name, max_name):
        return img_name >= min_name and img_name <= max_name

    def modifies_data(self):
        return True

    def preprocess(self):
        condition = list(self.settings["condition"].keys())[0]
        if condition == "project_datasets":
            project_datasets = self.settings["condition"][condition]
            for project_dataset_str in project_datasets:
                self._check_project_dataset_str(project_dataset_str)

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        h, w = ann.img_size

        condition = self.settings["condition"]
        satisfies_cond = False

        if "probability" in condition:
            prob = condition["probability"]
            satisfies_cond = random.random() < prob

        elif "regex_names" in condition:
            regex_names = condition["regex_names"]
            satisfies_cond = any(
                re.search(regex_name, img_desc.get_item_name()) for regex_name in regex_names
            )
            # @TODO: is it safe?

        elif "project_datasets" in condition:
            project_datasets = condition["project_datasets"]
            satisfies_cond = any(
                self._pr_ds_matches(project_dataset_str, img_desc)
                for project_dataset_str in project_datasets
            )

        elif "min_objects_count" in condition:
            thresh = condition["min_objects_count"]
            value = len(ann.labels)
            satisfies_cond = value >= thresh

        elif "include_classes" in condition:
            req_classes = condition["include_classes"]
            satisfies_cond = any(label.obj_class.name in req_classes for label in ann.labels)

        elif "tags" in condition:
            req_tags = condition["tags"]
            annotation_tag_names = set(tag.name for tag in ann.img_tags)
            satisfies_cond = len(annotation_tag_names & set(req_tags)) > 0

        elif "min_height" in condition:
            satisfies_cond = h >= condition["min_height"]

        elif "min_width" in condition:
            satisfies_cond = w >= condition["min_width"]

        elif "min_area" in condition:
            satisfies_cond = (h * w) >= condition["min_area"]

        elif "sum_object_area" in condition:
            thresh = condition["sum_object_area"]
            req_classes = condition["classes"]
            sum_area = sum(
                label.area for label in ann.labels if label.obj_class.name in req_classes
            )
            satisfies_cond = sum_area >= thresh

        elif "name_in_range" in condition:
            range = condition["name_in_range"]
            frame_step = condition["frame_step"]
            if self.is_image_name_in_range(img_desc.get_item_name(), range[0], range[1]):
                if self.frame_counter % frame_step == 0:
                    satisfies_cond = True
                self.frame_counter += 1

        if satisfies_cond:
            yield data_el + tuple([0])  # branch 0
        else:
            yield data_el + tuple([1])  # branch 1

# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation, ProjectMeta
from src.exceptions import BadSettingsError
from src.utils import get_project_by_name, get_project_meta

import src.globals as g


class FilteredProjectLayer(Layer):
    action = "filtered_project"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": [
                    "project_id",
                    "filtered_entities_ids",
                    "classes_mapping",
                    "tags_mapping",
                ],
                "properties": {
                    "project_id": {"type": "integer"},
                    "filtered_entities_ids": {"type": "array", "items": {"type": "integer"}},
                    "classes_mapping": {
                        "oneOf": [
                            {"type": "object", "patternProperties": {".*": {"type": "string"}}},
                            {"type": "string", "enum": ["default"]},
                        ]
                    },
                    "tags_mapping": {
                        "oneOf": [
                            {"type": "object", "patternProperties": {".*": {"type": "string"}}},
                            {"type": "string", "enum": ["default"]},
                        ]
                    },
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

        self._define_layer_project()
        if self.project_name is None:
            self.in_project_meta = ProjectMeta()
        else:
            self.in_project_meta = get_project_meta(get_project_by_name(self.project_name).id)

    def validate_source_connections(self):
        pass

    @classmethod
    def _split_data_src(cls, src):
        src_components = src.strip("/").split("/")
        if src_components == [""] or len(src_components) > 2:
            # Empty name or too many components.
            raise BadSettingsError(
                'Wrong "data" layer source path. Use "project_name/dataset_name" or "project_name/*"',
                extra={"layer_config": cls.config},
            )
        if len(src_components) == 1:
            # Only the project is specified, append '*' for the datasets.
            src_components.append("*")
        return src_components

    def _define_layer_project(self):
        self.project_name = None
        dataset_names = set()
        for src in self.srcs:
            project_name, dataset_name = self._split_data_src(src)
            if self.project_name is None:
                self.project_name = project_name
            elif self.project_name != project_name:
                raise BadSettingsError(
                    "Data Layer can only work with one project", extra={"layer_config": self.config}
                )
            dataset_names.add(dataset_name)
        self.dataset_names = list(dataset_names)

    def preprocess(self):
        return super().preprocess()

    def modifies_data(self):
        return False

    def process(self, data_el):
        yield data_el

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        yield data_els

    def has_batch_processing(self) -> bool:
        return True

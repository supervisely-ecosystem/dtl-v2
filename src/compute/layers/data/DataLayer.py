# coding: utf-8
from typing import Tuple

from supervisely import Annotation, Label, ProjectMeta

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.dtl_utils import apply_to_labels
from src.utils import get_project_by_name, get_project_meta
from src.exceptions import BadSettingsError


class DataLayer(Layer):
    action = "data"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_mapping"],
                "properties": {
                    "classes_mapping": {
                        "oneOf": [
                            {"type": "object", "patternProperties": {".*": {"type": "string"}}},
                            {"type": "string", "enum": ["default"]},
                        ]
                    }
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

    def define_classes_mapping(self):
        if self.settings.get("classes_mapping", "default") != "default":
            self.cls_mapping = self.settings["classes_mapping"]
        else:
            Layer.define_classes_mapping(self)

    def class_mapper(self, label: Label):
        curr_class = label.obj_class.name

        if curr_class in self.cls_mapping:
            new_class = self.cls_mapping[curr_class]
        else:
            raise BadSettingsError("Can not find mapping for class", extra={"class": curr_class})

        if new_class == ClassConstants.IGNORE:
            return []  # drop the figure
        elif new_class != ClassConstants.DEFAULT:
            obj_class = label.obj_class.clone(name=new_class)  # rename class
            label = label.clone(obj_class=obj_class)
        else:
            pass  # don't change
        return [label]

    def validate_source_connections(self):
        pass

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        ann = apply_to_labels(ann, self.class_mapper)
        yield (img_desc, ann)

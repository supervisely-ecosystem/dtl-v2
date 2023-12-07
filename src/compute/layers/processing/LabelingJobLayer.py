# coding: utf-8

from copy import deepcopy

from src.compute.Layer import Layer
import src.globals as g

# MAKE OUTPUT LAYER???

# 1 project name
# 2 checkbox keep original datasets structure | dataset name input


def _get_source_projects_ids_from_dtl():
    source_projects_ids = []
    for action in g.current_dtl_json:
        if action["action"] == "data":
            if len(action["src"]) == 0:
                continue
            project_name = action["src"][0].split("/")[0]
            project_id = g.api.project.get_info_by_name(g.WORKSPACE_ID, project_name).id
            source_projects_ids.append(project_id)
    return source_projects_ids


class LabelingJobLayer(Layer):
    action = "labeling_job"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": [
                    "name",
                    "description",
                    "readme",
                    "dataset_id",
                    "user_ids",
                    "reviewer_id",
                    "classes_to_label",
                    "tags_to_label",
                    "filter_condition",
                    "disable_objects_limit_per_item",
                    "objects_limit_per_item",
                    "disable_tags_limit_per_item",
                    "tags_limit_per_item",
                    "include_items_with_tags",
                    "exclude_items_with_tags",
                    "disable_items_range",
                    "items_range",
                    "items_ids",
                ],
                "properties": {
                    # description
                    "name": {
                        "type": "string",
                        "pattern": "^[0-9a-zA-Z \\-_]+$",
                    },
                    "description": {"type": "string"},
                    "readme": {"type": "string"},
                    "dataset_id": {"type": "integer"},
                    # members
                    "user_ids": {"type": "array", "items": {"type": "integer"}},
                    "reviewer_id": {"type": "integer"},
                    # classes
                    "classes_to_label": {"type": "array", "items": {"type": "string"}},
                    # tags
                    "tags_to_label": {"type": "array", "items": {"type": "string"}},
                    # filters
                    "filter_condition": {"type": "string", "enum": ["items", "condition"]},
                    "disable_objects_limit_per_item": {"type": "boolean"},
                    "objects_limit_per_item": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
                    "disable_tags_limit_per_item": {"type": "boolean"},
                    "tags_limit_per_item": {"oneOf": [{"type": "integer"}, {"type": "null"}]},
                    "include_items_with_tags": {"type": "array", "items": {"type": "string"}},
                    "exclude_items_with_tags": {"type": "array", "items": {"type": "string"}},
                    "disable_items_range": {"type": "boolean"},
                    "items_range": {
                        "oneOf": [{"type": "array", "items": {"type": "integer"}}, {"type": "null"}]
                    },
                    "items_ids": {"type": "array", "items": {"type": "integer"}},
                },
            },
        },
    }

    def __init__(self, config, output_folder, net):
        Layer.__init__(self, config, net=net)
        self.output_folder = output_folder
        self.sly_project_info = None

    def is_archive(self):
        return False

    def validate(self):
        super().validate()
        if len(self.settings.get("name", "")) > 2048:
            raise RuntimeError("Labeling Job name is too long")

    def validate_dest_connections(self):
        for dst in self.dsts:
            if len(dst) == 0:
                raise ValueError("Destination name in '{}' layer is empty!".format(self.action))

    def preprocess(self):
        if self.net.preview_mode:
            return
        if self.output_meta is None:
            raise GraphError(
                "Output meta is not set. Check that node is connected", extra={"layer": self.action}
            )
        if len(self.dsts) == 0:
            raise GraphError(
                "Destination is not set", extra={"layer_config": self.config, "layer": self.action}
            )
        dst = self.dsts[0]
        self.out_project_name = dst

        self.sly_project_info = g.api.project.create(
            g.WORKSPACE_ID,
            self.out_project_name,
            type=self.net.modality,
            change_name_if_conflict=True,
        )
        g.api.project.update_meta(self.sly_project_info.id, self.output_meta)

        custom_data = {
            "source_projects": _get_source_projects_ids_from_dtl(),
            "data-nodes": g.current_dtl_json,
        }
        g.api.project.update_custom_data(self.sly_project_info.id, custom_data)
        self.net_change_images = self.net.may_require_images()

    def process(self, data_el):
        img_desc, ann_orig = data_el
        new_img_desc = deepcopy(img_desc)

        name = self.settings.get("name", None)
        description = self.settings.get("description", None)
        readme = self.settings.get("readme", None)
        dataset_id = self.settings.get("dataset_id", None)
        user_ids = self.settings.get("user_ids", None)
        reviewer_id = self.settings.get("reviewer_id", None)
        classes_to_label = self.settings.get("classes_to_label", None)
        tags_to_label = self.settings.get("tags_to_label", None)
        filter_condition = self.settings.get("filter_condition", None)
        disable_objects_limit_per_item = self.settings.get("disable_objects_limit_per_item", None)
        objects_limit_per_item = self.settings.get("objects_limit_per_item", None)
        disable_tags_limit_per_item = self.settings.get("disable_tags_limit_per_item", None)
        tags_limit_per_item = self.settings.get("tags_limit_per_item", None)
        include_items_with_tags = self.settings.get("include_items_with_tags", None)
        exclude_items_with_tags = self.settings.get("exclude_items_with_tags", None)
        disable_items_range = self.settings.get("disable_items_range", None)
        items_range = self.settings.get("items_range", None)
        items_ids = self.settings.get("items_ids", None)

        if not self.net.preview_mode:
            g.api.labeling_job.create(
                name=name,
                dataset_id=dataset_id,
                user_ids=user_ids,
                readme=readme,
                description=description,
                classes_to_label=classes_to_label,
                objects_limit_per_image=objects_limit_per_item,
                tags_to_label=tags_to_label,
                tags_limit_per_image=tags_limit_per_item,
                include_images_with_tags=include_items_with_tags,
                exclude_images_with_tags=exclude_items_with_tags,
                images_range=items_range,
                reviewer_id=reviewer_id,
                images_ids=items_ids,
            )

        yield new_img_desc, ann_orig

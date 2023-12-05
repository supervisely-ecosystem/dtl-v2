# coding: utf-8

from copy import deepcopy

from src.compute.Layer import Layer
import src.globals as g


class LabelingJobLayer(Layer):
    action = "labeling_job"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "name": {
                    "type": "string",
                    "pattern": "^[0-9a-zA-Z \\-_]+$",
                },
                "dataset_id": {"type": "integer"},
                "user_ids": {"type": "array", "items": {"type": "integer"}},
                "readme": {"type": "string"},
                "description": {"type": "string"},
                "classes_to_label": {"type": "array", "items": {"type": "string"}},
                "objects_limit_per_image": {"type": "integer"},
                "tags_to_label": {"type": "array", "items": {"type": "string"}},
                "tags_limit_per_image": {"type": "integer"},
                "include_images_with_tags": {"type": "array", "items": {"type": "string"}},
                "exclude_images_with_tags": {"type": "array", "items": {"type": "string"}},
                "images_range": {"type": "array", "items": {"type": "integer"}},
                "reviewer_id": {"type": "integer"},
                "images_ids": {"type": "array", "items": {"type": "integer"}},
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        super().validate()
        if len(self.settings.get("name", "")) > 2048:
            raise RuntimeError("Labeling Job name is too long")

    def process(self, data_el):
        img_desc, ann_orig = data_el
        new_img_desc = deepcopy(img_desc)

        if not self.net.preview_mode:
            g.api.labeling_job.create(
                name=None,
                dataset_id=None,
                user_ids=None,
                readme=None,
                description=None,
                classes_to_label=None,
                objects_limit_per_image=None,
                tags_to_label=None,
                tags_limit_per_image=None,
                include_images_with_tags=None,
                exclude_images_with_tags=None,
                images_range=None,
                reviewer_id=None,
                images_ids=None,
            )

        yield new_img_desc, ann_orig

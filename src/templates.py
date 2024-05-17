from src.ui.tabs.presets import apply_json
import src.globals as g
from supervisely import ProjectInfo, DatasetInfo


project_info = None
project_name = None
src = None
if g.PROJECT_ID is not None:
    ds_name = "*"
    if g.DATASET_ID:
        ds: DatasetInfo = g.api.dataset.get_info_by_id(g.DATASET_ID)
        ds_name = ds.name
    pr: ProjectInfo = g.api.project.get_info_by_id(g.PROJECT_ID)
    src = [f"{pr.name}/{ds_name}"]
    project_info = pr
    project_name = pr.name


if len(g.FILTERED_ENTITIES) > 0:
    src_action = "filtered_project"
    src_action_template = (
        {
            "action": f"{src_action}",
            "src": src,
            "dst": f"${src_action}_1",
            "settings": {
                "project_id": g.PROJECT_ID,
                "filtered_entities_ids": g.FILTERED_ENTITIES,
                "classes_mapping": "default",
                "tags_mapping": "default",
            },
        },
    )
else:
    src_action = "images_project"
    src_action_template = (
        {
            "action": f"{src_action}",
            "src": src,
            "dst": f"${src_action}_1",
            "settings": {
                "classes_mapping": "default",
                "tags_mapping": "default",
            },
        },
    )

move = [
    {
        "action": f"{src_action}",
        "src": src,
        "dst": f"${src_action}_1",
        "settings": {
            "project_id": g.PROJECT_ID,
            "filtered_entities_ids": g.FILTERED_ENTITIES,
            "classes_mapping": "default",
            "tags_mapping": "default",
        },
    },
    {
        "action": "move",
        "src": [f"${src_action}_1"],
        "dst": "$move_2",
        "settings": {"move_confirmation": False},
    },
    {
        "action": "output_project",
        "src": ["$move_2"],
        "dst": [],
        "settings": {
            "is_existing_project": False,
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
        },
    },
]

copy = [
    {
        "action": f"{src_action}",
        "src": src,
        "dst": f"${src_action}_1",
        "settings": {
            "project_id": g.PROJECT_ID,
            "filtered_entities_ids": g.FILTERED_ENTITIES,
            "classes_mapping": "default",
            "tags_mapping": "default",
        },
    },
    {
        "action": "copy",
        "src": [f"${src_action}_1"],
        "dst": "$copy_2",
        "settings": {},
    },
    {
        "action": "output_project",
        "src": ["$copy_2"],
        "dst": [],
        "settings": {
            "is_existing_project": False,
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
        },
    },
]


obj_det_augs = [
    {
        "action": "images_project",
        "src": src,
        "dst": "$images_project_1",
        "settings": {"classes_mapping": "default", "tags_mapping": "default"},
        "scene_location": {"order_idx": 0, "position": {"x": 100, "y": 140}},
    },
    {
        "action": "if",
        "src": ["$images_project_1"],
        "dst": ["$if_3__true", "$if_3__false"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 1, "position": {"x": 594, "y": 139}},
    },
    {
        "action": "output_project",
        "src": ["$copy_5"],
        "dst": "qqqq",
        "settings": {
            "is_existing_project": False,
            "project_name": f"{project_name} (augmented)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
        },
        "scene_location": {"order_idx": 2, "position": {"x": 2134, "y": 110}},
    },
    {
        "action": "copy",
        "src": ["$iaa_imgcorruptlike_blur_7", "$iaa_imgcorruptlike_noise_6"],
        "dst": "$copy_5",
        "settings": {},
        "scene_location": {"order_idx": 3, "position": {"x": 1709, "y": 171}},
    },
    {
        "action": "iaa_imgcorruptlike_noise",
        "src": ["$if_3__true"],
        "dst": "$iaa_imgcorruptlike_noise_6",
        "settings": {"option": "gaussian_noise", "severity": 2},
        "scene_location": {"order_idx": 4, "position": {"x": 1115, "y": -190}},
    },
    {
        "action": "iaa_imgcorruptlike_blur",
        "src": ["$if_3__false"],
        "dst": "$iaa_imgcorruptlike_blur_7",
        "settings": {"option": "defocus_blur", "severity": 2},
        "scene_location": {"order_idx": 5, "position": {"x": 1102, "y": 389}},
    },
]


def load_template(template):
    apply_json(template)


templates = {
    "images": {"move": move, "copy": copy, "obj_det_augs": obj_det_augs},
    "videos": {},
}

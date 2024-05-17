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
        "dst": ["$if_3__true", "$if_3__False"],
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
        "src": ["$if_3__False"],
        "dst": "$iaa_imgcorruptlike_blur_7",
        "settings": {"option": "defocus_blur", "severity": 2},
        "scene_location": {"order_idx": 5, "position": {"x": 1102, "y": 389}},
    },
]

obj_det_augs2 = [
    {
        "action": "images_project",
        "src": src,
        "dst": "$images_project_1",
        "settings": {"classes_mapping": "default", "tags_mapping": "default"},
        "scene_location": {"order_idx": 0, "position": {"x": -727, "y": 231}},
    },
    {
        "action": "random_color",
        "src": ["$if_9__true"],
        "dst": "$random_color_2",
        "settings": {"strength": 0.2},
        "scene_location": {"order_idx": 1, "position": {"x": 2208, "y": -75}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_13__true"],
        "dst": "$contrast_brightness_3",
        "settings": {
            "contrast": {"min": 0.4, "max": 1.3, "center_grey": False},
            "brightness": {"min": 0, "max": 0},
        },
        "scene_location": {"order_idx": 2, "position": {"x": 3877, "y": -530}},
    },
    {
        "action": "noise",
        "src": ["$if_16__true"],
        "dst": "$noise_4",
        "settings": {"mean": 0, "std": 12},
        "scene_location": {"order_idx": 3, "position": {"x": 5802, "y": -273}},
    },
    {
        "action": "crop",
        "src": ["$images_project_1"],
        "dst": "$crop_5",
        "settings": {
            "random_part": {
                "height": {"min_percent": 40, "max_percent": 100},
                "width": {"min_percent": 40, "max_percent": 100},
                "keep_aspect_ratio": False,
            }
        },
        "scene_location": {"order_idx": 4, "position": {"x": -194, "y": 230}},
    },
    {
        "action": "resize",
        "src": ["$crop_5"],
        "dst": "$resize_6",
        "settings": {"width": 512, "height": 512, "aspect_ratio": {"keep": False}},
        "scene_location": {"order_idx": 5, "position": {"x": 280, "y": 227}},
    },
    {
        "action": "flip",
        "src": ["$if_8__true"],
        "dst": "$flip_7",
        "settings": {"axis": "horizontal"},
        "scene_location": {"order_idx": 6, "position": {"x": 1271, "y": -316}},
    },
    {
        "action": "if",
        "src": ["$resize_6"],
        "dst": ["$if_8__true", "$if_8__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 7, "position": {"x": 746, "y": 226}},
    },
    {
        "action": "if",
        "src": ["$flip_7", "$if_8__False"],
        "dst": ["$if_9__true", "$if_9__False"],
        "settings": {"condition": {"probability": 0.35}},
        "scene_location": {"order_idx": 8, "position": {"x": 1727, "y": 248}},
    },
    {
        "action": "if",
        "src": ["$random_color_2", "$if_9__False"],
        "dst": ["$if_10__true", "$if_10__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 9, "position": {"x": 2619, "y": 269}},
    },
    {
        "action": "if",
        "src": [
            "$if_12__False",
            "$contrast_brightness_3",
            "$if_13__False",
            "$contrast_brightness_14",
        ],
        "dst": ["$if_11__true", "$if_11__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 10, "position": {"x": 4393, "y": 164}},
    },
    {
        "action": "if",
        "src": ["$if_10__False"],
        "dst": ["$if_12__true", "$if_12__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 11, "position": {"x": 3275, "y": 487}},
    },
    {
        "action": "if",
        "src": ["$if_10__true"],
        "dst": ["$if_13__true", "$if_13__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 12, "position": {"x": 3268, "y": 122}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_12__true"],
        "dst": "$contrast_brightness_14",
        "settings": {
            "contrast": {"min": 1, "max": 1, "center_grey": False},
            "brightness": {"min": -80, "max": 80},
        },
        "scene_location": {"order_idx": 13, "position": {"x": 3875, "y": 558}},
    },
    {
        "action": "blur",
        "src": ["$if_11__true"],
        "dst": "$blur_15",
        "settings": {"name": "gaussian", "sigma": {"min": 1, "max": 3}},
        "scene_location": {"order_idx": 14, "position": {"x": 4950, "y": -274}},
    },
    {
        "action": "if",
        "src": ["$blur_15", "$if_11__False"],
        "dst": ["$if_16__true", "$if_16__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 15, "position": {"x": 5269, "y": 685}},
    },
    {
        "action": "output_project",
        "src": ["$if_16__False", "$noise_4"],
        "dst": "coco2017 (augmented)",
        "settings": {
            "project_name": f"{project_name} (augmented)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
            "is_existing_project": False,
        },
        "scene_location": {"order_idx": 16, "position": {"x": 6538, "y": 494}},
    },
]


def load_template(template):
    apply_json(template)


templates = {
    "images": {
        "move": move,
        "copy": copy,
        "obj_det_augs": obj_det_augs,
        "obj_det_augs2": obj_det_augs2,
    },
    "videos": {},
}

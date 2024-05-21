import src.globals as g
from src.preconfigured.utils import get_src, get_src_action

src, project_info, project_name = get_src()
src_action, src_action_template = get_src_action(src)


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
            "project_name": f"{project_name} (move)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
            "is_existing_project": False,
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
            "project_name": f"{project_name} (copy)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
            "is_existing_project": False,
        },
    },
]


basic_detection_augmentations = [
    {
        **src_action_template,
        "scene_location": {"order_idx": 0, "position": {"x": 100, "y": 140}},
    },
    {
        "action": "if",
        "src": [f"${src_action}_1"],
        "dst": ["$if_2__true", "$if_2__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 1, "position": {"x": 550, "y": 140}},
    },
    {
        "action": "crop",
        "src": ["$if_2__true"],
        "dst": "$crop_3",
        "settings": {
            "random_part": {
                "height": {"min_percent": 50, "max_percent": 100},
                "width": {"min_percent": 50, "max_percent": 100},
                "keep_aspect_ratio": False,
            }
        },
        "scene_location": {"order_idx": 2, "position": {"x": 1000, "y": -210}},
    },
    {
        "action": "resize",
        "src": ["$if_2__False", "$crop_3"],
        "dst": "$resize_4",
        "settings": {"width": 512, "height": 512, "aspect_ratio": {"keep": False}},
        "scene_location": {"order_idx": 3, "position": {"x": 1450, "y": 140}},
    },
    {
        "action": "if",
        "src": ["$resize_4"],
        "dst": ["$if_5__true", "$if_5__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 4, "position": {"x": 1900, "y": 140}},
    },
    {
        "action": "flip",
        "src": ["$if_5__true"],
        "dst": "$flip_6",
        "settings": {"axis": "horizontal"},
        "scene_location": {"order_idx": 5, "position": {"x": 2350, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$if_5__False", "$flip_6"],
        "dst": ["$if_7__true", "$if_7__False"],
        "settings": {"condition": {"probability": 0.35}},
        "scene_location": {"order_idx": 6, "position": {"x": 2800, "y": 140}},
    },
    {
        "action": "random_color",
        "src": ["$if_7__true"],
        "dst": "$random_color_8",
        "settings": {"strength": 0.2},
        "scene_location": {"order_idx": 7, "position": {"x": 3250, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$if_7__False", "$random_color_8"],
        "dst": ["$if_9__true", "$if_9__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 8, "position": {"x": 3700, "y": 140}},
    },
    {
        "action": "if",
        "src": ["$if_9__true"],
        "dst": ["$if_10__true", "$if_10__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 9, "position": {"x": 4050, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$if_9__False"],
        "dst": ["$if_11__true", "$if_11__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 10, "position": {"x": 4050, "y": 490}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_10__true"],
        "dst": "$contrast_brightness_12",
        "settings": {
            "contrast": {"min": 0.4, "max": 1.3, "center_grey": False},
            "brightness": {"min": 0, "max": 0},
        },
        "scene_location": {"order_idx": 11, "position": {"x": 4500, "y": -210}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_11__true"],
        "dst": "$contrast_brightness_13",
        "settings": {
            "contrast": {"min": 1, "max": 1, "center_grey": False},
            "brightness": {"min": -80, "max": 80},
        },
        "scene_location": {"order_idx": 12, "position": {"x": 4500, "y": 490}},
    },
    {
        "action": "if",
        "src": [
            "$if_10__False",
            "$if_11__False",
            "$contrast_brightness_13",
            "$contrast_brightness_12",
        ],
        "dst": ["$if_14__true", "$if_14__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 13, "position": {"x": 4950, "y": 140}},
    },
    {
        "action": "blur",
        "src": ["$if_14__true"],
        "dst": "$blur_15",
        "settings": {"name": "gaussian", "sigma": {"min": 1, "max": 3}},
        "scene_location": {"order_idx": 14, "position": {"x": 5400, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$if_14__False", "$blur_15"],
        "dst": ["$if_16__true", "$if_16__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 15, "position": {"x": 5850, "y": 140}},
    },
    {
        "action": "noise",
        "src": ["$if_16__true"],
        "dst": "$noise_17",
        "settings": {"mean": 0, "std": 12},
        "scene_location": {"order_idx": 16, "position": {"x": 6300, "y": -210}},
    },
    {
        "action": "copy",
        "src": ["$if_16__False", "$noise_17"],
        "dst": "$copy_18",
        "settings": {},
        "scene_location": {"order_idx": 17, "position": {"x": 6750, "y": 140}},
    },
    {
        "action": "output_project",
        "src": ["$copy_18"],
        "dst": [],
        "settings": {
            "project_name": f"{project_name} (augmented)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
            "is_existing_project": False,
        },
        "scene_location": {"order_idx": 18, "position": {"x": 7200, "y": 140}},
    },
]

basic_segmentation_augmentations = [
    {
        **src_action_template,
        "scene_location": {"order_idx": 0, "position": {"x": 100, "y": 140}},
    },
    {
        "action": "if",
        "src": [f"${src_action}_1"],
        "dst": ["$if_2__true", "$if_2__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 1, "position": {"x": 550, "y": 140}},
    },
    {
        "action": "rotate",
        "src": ["$if_2__true"],
        "dst": "$rotate_3",
        "settings": {
            "rotate_angles": {"min_degrees": -30, "max_degrees": 30},
            "black_regions": {"mode": "preserve_size"},
        },
        "scene_location": {"order_idx": 2, "position": {"x": 1000, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$rotate_3", "$if_2__False"],
        "dst": ["$if_4__true", "$if_4__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 3, "position": {"x": 1450, "y": 140}},
    },
    {
        "action": "crop",
        "src": ["$if_4__true"],
        "dst": "$crop_5",
        "settings": {
            "random_part": {
                "height": {"min_percent": 60, "max_percent": 100},
                "width": {"min_percent": 60, "max_percent": 100},
                "keep_aspect_ratio": False,
            }
        },
        "scene_location": {"order_idx": 4, "position": {"x": 1900, "y": -210}},
    },
    {
        "action": "resize",
        "src": ["$crop_5", "$if_4__False"],
        "dst": "$resize_6",
        "settings": {"width": 512, "height": 512, "aspect_ratio": {"keep": False}},
        "scene_location": {"order_idx": 5, "position": {"x": 2350, "y": 140}},
    },
    {
        "action": "if",
        "src": ["$resize_6"],
        "dst": ["$if_7__true", "$if_7__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 6, "position": {"x": 2800, "y": 140}},
    },
    {
        "action": "flip",
        "src": ["$if_7__true"],
        "dst": "$flip_8",
        "settings": {"axis": "horizontal"},
        "scene_location": {"order_idx": 7, "position": {"x": 3250, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$flip_8", "$if_7__False"],
        "dst": ["$if_9__true", "$if_9__False"],
        "settings": {"condition": {"probability": 0.35}},
        "scene_location": {"order_idx": 8, "position": {"x": 3700, "y": 140}},
    },
    {
        "action": "random_color",
        "src": ["$if_9__true"],
        "dst": "$random_color_10",
        "settings": {"strength": 0.2},
        "scene_location": {"order_idx": 9, "position": {"x": 4150, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$random_color_10", "$if_9__False"],
        "dst": ["$if_11__true", "$if_11__False"],
        "settings": {"condition": {"probability": 0.5}},
        "scene_location": {"order_idx": 10, "position": {"x": 4600, "y": 140}},
    },
    {
        "action": "if",
        "src": ["$if_11__true"],
        "dst": ["$if_12__true", "$if_12__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 11, "position": {"x": 5050, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$if_11__False"],
        "dst": ["$if_13__true", "$if_13__False"],
        "settings": {"condition": {"probability": 0.2}},
        "scene_location": {"order_idx": 12, "position": {"x": 5050, "y": 490}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_12__true"],
        "dst": "$contrast_brightness_14",
        "settings": {
            "contrast": {"min": 0.4, "max": 1.3, "center_grey": False},
            "brightness": {"min": 0, "max": 0},
        },
        "scene_location": {"order_idx": 13, "position": {"x": 5500, "y": -210}},
    },
    {
        "action": "contrast_brightness",
        "src": ["$if_13__true"],
        "dst": "$contrast_brightness_15",
        "settings": {
            "contrast": {"min": 1, "max": 1, "center_grey": False},
            "brightness": {"min": -80, "max": 80},
        },
        "scene_location": {"order_idx": 14, "position": {"x": 5500, "y": 490}},
    },
    {
        "action": "if",
        "src": [
            "$contrast_brightness_14",
            "$if_12__False",
            "$contrast_brightness_15",
            "$if_13__False",
        ],
        "dst": ["$if_16__true", "$if_16__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 15, "position": {"x": 5950, "y": 140}},
    },
    {
        "action": "blur",
        "src": ["$if_16__true"],
        "dst": "$blur_17",
        "settings": {"name": "gaussian", "sigma": {"min": 1, "max": 3}},
        "scene_location": {"order_idx": 16, "position": {"x": 6400, "y": -210}},
    },
    {
        "action": "if",
        "src": ["$blur_17", "$if_16__False"],
        "dst": ["$if_18__true", "$if_18__False"],
        "settings": {"condition": {"probability": 0.3}},
        "scene_location": {"order_idx": 17, "position": {"x": 6850, "y": 140}},
    },
    {
        "action": "noise",
        "src": ["$if_18__true"],
        "dst": "$noise_19",
        "settings": {"mean": 0, "std": 12},
        "scene_location": {"order_idx": 18, "position": {"x": 7300, "y": -210}},
    },
    {
        "action": "copy",
        "src": ["$noise_19", "$if_18__False"],
        "dst": "$copy_20",
        "settings": {},
        "scene_location": {"order_idx": 19, "position": {"x": 7750, "y": 140}},
    },
    {
        "action": "output_project",
        "src": ["$copy_20"],
        "dst": [],
        "settings": {
            "project_name": f"{project_name} (augmented)",
            "dataset_option": "new",
            "dataset_name": "",
            "dataset_id": None,
            "merge_different_meta": False,
            "is_existing_project": False,
        },
        "scene_location": {"order_idx": 20, "position": {"x": 8200, "y": 140}},
    },
]

templates = {
    "images": {
        "move": move,
        "copy": copy,
        "basic-detection-augmentations": basic_detection_augmentations,
        "basic-segmentation-augmentation": basic_segmentation_augmentations,  # key to be renamed soon
        "basic-segmentation-augmentations": basic_segmentation_augmentations,
    },
    "videos": {},
}

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

move = [
    {
        "action": "filtered_project",
        "src": src,
        "dst": "$filtered_project_1",
        "settings": {
            "project_id": g.PROJECT_ID,
            "filtered_entities_ids": g.FILTERED_ENTITIES,
            "classes_mapping": "default",
            "tags_mapping": "default",
        },
    },
    {
        "action": "move",
        "src": ["$filtered_project_1"],
        "dst": "$move_2",
        "settings": {"move_confirmation": False},
    },
    {
        "action": "supervisely_project",
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
        "action": "filtered_project",
        "src": src,
        "dst": "$filtered_project_1",
        "settings": {
            "project_id": g.PROJECT_ID,
            "filtered_entities_ids": g.FILTERED_ENTITIES,
            "classes_mapping": "default",
            "tags_mapping": "default",
        },
    },
    {
        "action": "copy",
        "src": ["$filtered_project_1"],
        "dst": "$copy_2",
        "settings": {},
    },
    {
        "action": "supervisely_project",
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


def load_template(template):
    apply_json(template)


templates = {
    "images": {
        "move": move,
        "copy": copy,
    },
    "videos": {},
}

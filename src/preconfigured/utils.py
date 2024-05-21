from src.ui.tabs.presets import apply_json
import src.globals as g
from supervisely import ProjectInfo, DatasetInfo


def get_src():
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

    return src, project_info, project_name


def get_src_action(src):
    if len(g.FILTERED_ENTITIES) > 0:
        src_action = "filtered_project"
        src_action_template = {
            "action": f"{src_action}",
            "src": src,
            "dst": f"${src_action}_1",
            "settings": {
                "project_id": g.PROJECT_ID,
                "filtered_entities_ids": g.FILTERED_ENTITIES,
                "classes_mapping": "default",
                "tags_mapping": "default",
            },
        }
    else:
        src_action = "images_project"
        src_action_template = {
            "action": f"{src_action}",
            "src": src,
            "dst": f"${src_action}_1",
            "settings": {
                "classes_mapping": "default",
                "tags_mapping": "default",
            },
        }
    return src_action, src_action_template


def load_template(template):
    apply_json(template)

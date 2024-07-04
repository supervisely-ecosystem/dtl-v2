from typing import List
from supervisely.api.api import Api
from supervisely.app.widgets import (
    AgentSelector,
    Button,
    Text,
    Select,
    RadioTabs,
    RadioGroup,
    CustomModelsSelector,
    PretrainedModelsSelector,
    Checkbox,
)

from supervisely.api.agent_api import AgentInfo
from supervisely.api.app_api import SessionInfo
import src.globals as g
import supervisely as sly
import os
from collections import OrderedDict
from cache import get_random_image

augs_configs = sly.json.load_json_file(os.path.join(os.getcwd(), "augs.json"))
meta = g.api.project.get_meta(g.PROJECT_ID)

pipeline = []

images_info = {}
all_images = []


def _normalize_params(default_params: dict, params: dict):
    ptypes = {p["pname"]: p for p in default_params}
    res = OrderedDict()
    for name, value in params.items():
        if ptypes[name]["type"] == "el-slider-range":
            res[name] = tuple(value)
        elif (
            ptypes[name]["type"] == "el-input-number" and ptypes[name].get("valueType") is not None
        ):
            try:
                res[name] = int(value)
            except ValueError as e:
                res[name] = int(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-number":
            try:
                res[name] = float(value)
            except ValueError as e:
                res[name] = float(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-range":
            try:
                res[name] = tuple([int(value[0]), int(value[1])])
            except ValueError as e:
                res[name] = tuple(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-number-range":
            try:
                res[name] = [int(value[0]), int(value[1])]
                res[name].sort()
                res[name] = tuple(res[name])
            except ValueError as e:
                res[name] = tuple(ptypes[name]["default"])
        else:
            res[name] = value
    return res


def get_aug_info(state):
    category_name = state["category"]
    aug_name = state["aug"]
    ui_defaults = augs_configs[category_name][aug_name]["params"]
    ui_vmodels = state["augVModels"][category_name][aug_name]
    sometimes = float(state["sometimesP"]) if state["sometimes"] else None
    params = _normalize_params(ui_defaults, ui_vmodels)
    aug_info = sly.imgaug_utils.create_aug_info(category_name, aug_name, params, sometimes)
    return aug_info


def save_preview_image(api: sly.Api, task_id, img):
    local_path = g.PREVIEW_DIR
    remote_path = os.path.join(f"/imgaug_studio/{task_id}", f"last_preview.png")
    sly.image.write(local_path, img)
    if api.file.exists(g.TEAM_ID, remote_path):
        api.file.remove(g.TEAM_ID, remote_path)
    file_info = api.file.upload(g.TEAM_ID, local_path, remote_path)
    return file_info

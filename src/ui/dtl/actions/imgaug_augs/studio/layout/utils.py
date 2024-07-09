import os
import json
from collections import OrderedDict
from typing import List, Dict
from supervisely.app.widgets import (
    Select,
    Checkbox,
    Input,
    InputNumber,
    Slider,
    Widget,
    Field,
)
import supervisely as sly

import src.globals as g


json_path = os.path.join(
    os.getcwd(), "src", "ui", "dtl", "actions", "imgaug_augs", "studio", "layout", "augs.json"
)

augs_configs = sly.json.load_json_file(json_path)
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


json_path = os.path.join(os.getcwd(), "src/ui/dtl/actions/imgaug_augs/studio/layout/augs.json")

augs_json = ""
with open(json_path, "r") as file:
    augs_json = json.load(file)


def get_params_widget(category, func):
    def _get_select_items_params(options):
        return [Select.Item(option, option) for option in options]

    json_data = augs_json.get(category)
    if json_data is None:
        raise ValueError(f"Json has no category {category}")
    augmenter_data = json_data.get(func)
    if augmenter_data is None:
        return None

    html_to_widget = {
        "el-input-number": InputNumber,
        "el-input-number-range": Input,
        "el-select": Select,
        "el-slider-range": Slider,
        "el-checkbox": Checkbox,
    }
    ignore = ["pname", "type", "valueType"]

    fields = []
    for param in augmenter_data["params"]:
        param_name = param["pname"]
        param_type = param["type"]
        widget = html_to_widget.get(param_type)
        if widget is None:
            raise ValueError("widget not found")
        filtered_param = {}
        for k, v in param.items():
            if k not in ignore:
                if k == "default":
                    if param_type == "el-checkbox":
                        filtered_param["checked"] = v
                        filtered_param["content"] = param_name
                    else:
                        filtered_param["value"] = v
                elif k == "options":
                    filtered_param["items"] = _get_select_items_params(param["options"])
                    del filtered_param["value"]
            if param_type == "el-input-number-range" or param_type == "el-slider-range":
                filtered_param["range"] = True

        widget_obj = widget(**filtered_param)
        field = Field(widget_obj, param_name)
        fields.append(field)
    return fields


def get_params_from_widgets(widgets: List[Widget]) -> Dict:
    params = {}
    for field_widget in widgets:
        field_widget: Field
        param_name = field_widget._title
        widget = field_widget._content
        if isinstance(widget, Select):
            params[param_name] = widget.get_value()
        elif isinstance(widget, Input):
            params[param_name] = widget.get_value()
        elif isinstance(widget, InputNumber):
            params[param_name] = widget.get_value()
        elif isinstance(widget, Slider):
            params[param_name] = widget.get_value()
        elif isinstance(widget, Checkbox):
            params[param_name] = widget.is_checked()
        else:
            raise ValueError(f"Unknown widget type: {widget}")
    return params

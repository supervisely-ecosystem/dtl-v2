import os
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
from supervisely.io.json import load_json_file


json_path = os.path.join(os.getcwd(), "src/ui/dtl/actions/imgaug_augs/studio/layout/augs.json")
augs_json = load_json_file(json_path)


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
        "el-input-number-range": Slider,
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
                else:
                    filtered_param[k] = v
        if widget == Slider:
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

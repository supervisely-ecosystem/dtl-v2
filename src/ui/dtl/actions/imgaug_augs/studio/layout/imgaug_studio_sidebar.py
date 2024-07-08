from src.ui.widgets.augs_list import AugsList
from supervisely.app.widgets import (
    NodesFlow,
    Container,
    Button,
    Text,
    Field,
    Select,
    Checkbox,
    Slider,
    Input,
    InputNumber,
)
import os
import json

json_path = os.path.join(os.getcwd(), "src/ui/dtl/actions/imgaug_augs/studio/layout/augs.json")

augs_json = ""
with open(json_path, "r") as file:
    augs_json = json.load(file)


def _get_params_widget(category, func):
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


def create_sidebar_widgets():

    # sidebar aug layout
    pipeline_widget = AugsList()
    add_aug_button = Button("ADD", icon="zmdi zmdi-playlist-plus mr5", button_size="small")
    pipeline_sidebar_container = Container(widgets=[pipeline_widget, add_aug_button])
    pipeline_sidebar_field = Field(
        pipeline_sidebar_container,
        title="Your custom augmentation pipeline",
        description="Add transformations in a sequence, preview the results of individual aug or a whole pipeline",
    )
    pipeline_sidebar_field.hide()

    # category field
    aug_category_items = [Select.Item(category, category) for category in augs_json]
    aug_category_selector = Select(aug_category_items)
    aug_category_field = Field(
        aug_category_selector, "Augmenter Category", "Choose augmentation category"
    )
    aug_funcs_list = augs_json.get(aug_category_selector.get_value())
    aug_funcs_list = aug_funcs_list.keys()
    aug_func_items = [Select.Item(func, func) for func in aug_funcs_list]
    aug_func_selector = Select(aug_func_items)
    aug_func_field = Field(aug_func_selector, "Transformation", "Choose augmentation function")
    # --------------------------

    # probability field
    DEFAULT_SOMETIMES_VALUE = 0.5
    aug_sometimes_check = Checkbox(content="probability")
    aug_sometimes_input = InputNumber(DEFAULT_SOMETIMES_VALUE, 0, 1, 0.01)
    aug_sometimes_input.disable()
    aug_sometimes_container = Container([aug_sometimes_check, aug_sometimes_input], "horizontal")
    aug_sometimes_field = Field(
        aug_sometimes_container, "Apply sometimes", "apply aug with given probability"
    )

    # params field
    params_fields = _get_params_widget(
        aug_category_selector.get_value(), aug_func_selector.get_value()
    )

    fields_container = Container(params_fields)
    aug_params_field = Field(
        fields_container,
        "Params",
        "Configure current augmentation",
    )

    # complete add aug field
    aug_add_to_pipeline_button = Button("ADD TO PIPELINE", icon="zmdi zmdi-check")
    aug_add_container = Container(
        [
            aug_category_field,
            aug_func_field,
            aug_sometimes_field,
            aug_params_field,
            aug_add_to_pipeline_button,
        ]
    )
    aug_add_field = Field(
        aug_add_container, "Add aug to pipeline", "Explore, configure and preview"
    )

    return (
        pipeline_widget,
        add_aug_button,
        pipeline_sidebar_container,
        pipeline_sidebar_field,
        aug_category_selector,
        aug_category_field,
        aug_func_items,
        aug_func_selector,
        aug_func_field,
        aug_sometimes_check,
        aug_sometimes_input,
        aug_sometimes_container,
        aug_sometimes_field,
        fields_container,
        aug_params_field,
        aug_add_to_pipeline_button,
        aug_add_container,
        aug_add_field,
        params_fields,
    )

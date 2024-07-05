from typing import Optional
from os.path import realpath, dirname
from supervisely import logger
from supervisely.nn.inference.session import Session

from src.ui.dtl.utils import (
    get_layer_docs,
    get_text_font_size,
    get_slider_style,
    classes_list_to_mapping,
)

from src.ui.dtl.Layer import Layer

from src.ui.dtl.actions.imgaug_augs.studio.layout.node_layout import create_node_layout
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as utils
import src.globals as g
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
import src.globals as g
import supervisely as sly
import os


class ImgAugStudioAction(Layer):
    name = "imgaug_studio_action"
    title = "ImgAug Studio"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    model_params = {}

    @classmethod
    def create_inputs(self):
        return []

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        return Layer(
            action=cls,
            id=layer_id,
            need_preview=False,
            init_widgets=cls.init_widgets,
        )

    @classmethod
    def init_widgets(cls, layer: Layer):
        saved_settings = {}
        session: Session = None

        def _get_params_json(json_data, aug_func):
            if json_data is None or aug_func not in json_data:
                return None

            html_to_widget = {
                "el-input-number": InputNumber,
                "el-input-number-range": Input,
                "el-select": Select,
                "el-slider-range": Slider,
                "el-checkbox": Checkbox,
            }

            augmenter_data = json_data[aug_func]

            fields = []
            for param in augmenter_data["params"]:
                param_name = param["pname"]
                param_type = param["type"]
                widget = html_to_widget.get(param_type)
                if widget is None:
                    raise ValueError("widget not found")

                filtered_param = {k: v for k, v in param.items() if k != "pname"}
                widget_obj = widget(**filtered_param)
                field = Field(widget_obj, param_name)
                fields.append(field)

            return fields

        def get_set_settings_button_style():
            return "flex: auto; border: 1px solid #bfcbd9; color: black; background-color: white;"

        def get_text_font_size():
            return 13

        pipeline_layout_text = Text("Select agent", status="text", font_size=get_text_font_size())
        pipeline_layout_edit_button = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        pipeline_layout_container = Container(
            widgets=[pipeline_layout_text, pipeline_layout_edit_button],
            direction="horizontal",
            style="place-items: center",
        )

        pipeline_widget = AugsList()

        add_aug_button = Button("ADD", icon="zmdi zmdi-playlist-plus mr5", button_size="small")

        pipeline_sidebar_container = Container(widgets=[pipeline_widget, add_aug_button])

        pipeline_sidebar_field = Field(
            pipeline_sidebar_container,
            title="Your custom augmentation pipeline",
            description="Add transformations in a sequence, preview the results of individual aug or a whole pipeline",
        )

        from src.ui.dtl.actions.imgaug_augs.studio.layout.allowed_augs import augs_modules

        aug_category_items = [Select.Item(category, category) for category in augs_modules]
        aug_category_selector = Select(aug_category_items)
        aug_category_field = Field(
            aug_category_selector, "Augmenter Category", "Choose augmentation category"
        )
        aug_funcs_list = augs_modules.get(aug_category_selector.get_value())
        aug_func_items = [
            Select.Item(value=func, label=f"{func.__name__}") for func in aug_funcs_list
        ]
        aug_func_selector = Select(aug_func_items)
        aug_func_field = Field(aug_func_selector, "Transformation", "Choose augmentation function")

        DEFAULT_SOMETIMES_VALUE = 0.5
        aug_sometimes_check = Checkbox(Text("probability"))
        aug_sometimes_input = InputNumber(DEFAULT_SOMETIMES_VALUE, 0, 1, 0.01)
        aug_sometimes_input.disable()
        aug_sometimes_container = Container(
            [aug_sometimes_check, aug_sometimes_input], "horizontal"
        )
        aug_sometimes_field = Field(
            aug_sometimes_container, "Apply sometimes", "apply aug with given probability"
        )

        json_data = augs_modules.get(aug_category_selector.get_value())
        widgets = _get_params_json(json_data, aug_func_selector.get_value())
        fields_container = Container(widgets)
        aug_params_field = Field(
            fields_container,
            "Params",
            "Configure current augmentation",
        )

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
        aug_add_field.hide()

        @pipeline_layout_edit_button.click
        def pipeline_layout_edit_button_cb():
            pipeline_layout_edit_button.disable()
            aug_add_field.show()  # todo

        @add_aug_button.click
        def add_button_cb():
            category = aug_category_selector.get_value()
            method = aug_func_selector.get_value()
            params = [widget.get_value() for widget in widgets]
            if aug_sometimes_check.is_checked():
                sometimes = aug_sometimes_input.get_value()
            else:
                sometimes = None
            pipeline_widget.append(AugsList.AugItem(category, method, params, sometimes))
            saved_settings["pipeline"] = pipeline_widget.get_pipeline()
            aug_add_field.hide()
            pipeline_layout_edit_button.enable()

        @aug_sometimes_check.value_changed
        def aug_sometimes_check_cb():
            if aug_sometimes_check.is_checked():
                aug_sometimes_input.enable()
            elif aug_sometimes_check.is_checked is False:
                aug_sometimes_input.disable()

        @aug_category_selector.value_changed()
        def aug_category_selector_cb():
            new_value = aug_category_selector.get_value()
            new_funcs = augs_modules.get(new_value)
            aug_func_selector.set(new_funcs)

        def data_changed_cb(**kwargs):
            pass

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def get_data() -> dict:
            nonlocal session
            data = {}
            if session is not None:
                data["session_id"] = session.task_id
            data["deploy_layer_name"] = layer.action.title
            return data

        def _set_settings_from_json(settings: dict):
            pass

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = create_node_layout(pipeline_layout_container, pipeline_sidebar_field)
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        layer._create_options = create_options
        layer._get_settings = get_settings
        layer._get_data = get_data

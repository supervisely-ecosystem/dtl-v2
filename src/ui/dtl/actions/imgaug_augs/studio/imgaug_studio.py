from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


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
from supervisely.app import StateJson, DataJson
from src.ui.dtl import ImgAugAugmentationsAction
from src.ui.widgets.augs_list import AugsList
import os
import json
from src.ui.dtl.utils import (
    get_text_font_size,
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
)

from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_sidebar import (
    create_sidebar_widgets,
    augs_json,
    _get_params_widget,
)


class ImgAugStudioAction(ImgAugAugmentationsAction):
    name = "imgaug_studio"
    title = "ImgAug Studio"
    docs_url = ""
    description = "ImgAug Studio app in a node format."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        saved_settings = {"pipeline": {}}

        # layout edit button
        pipeline_layout_text = Text(
            "Edit Augmentation Pipeline", status="text", font_size=get_text_font_size()
        )
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

        (
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
        ) = create_sidebar_widgets()
        aug_add_field.hide()

        # @TODO: two fields in the sidebar, add aug field in layout instead of sidebar

        @pipeline_layout_edit_button.click
        def pipeline_layout_edit_button_cb():
            pipeline_layout_edit_button.disable()
            pipeline_sidebar_field.show()

        @aug_add_to_pipeline_button.click
        def aug_add_to_pipeline_button_cb():
            nonlocal params_fields
            category = aug_category_selector.get_value()
            method = aug_func_selector.get_value()
            params = [field for field in params_fields]  # todo
            if aug_sometimes_check.is_checked():
                sometimes = aug_sometimes_input.get_value()
            else:
                sometimes = None
            pipeline_widget.append(AugsList.AugItem(category, method, params, sometimes))
            saved_settings["pipeline"] = pipeline_widget.get_pipeline()
            aug_add_field.hide()
            add_aug_button.enable()
            pipeline_layout_edit_button.enable()

        @add_aug_button.click
        def add_aug_button_cb():
            aug_add_field.show()
            add_aug_button.disable()

        @aug_sometimes_check.value_changed
        def aug_sometimes_check_cb(value):
            if value is True:
                aug_sometimes_input.enable()
            elif value is False:
                aug_sometimes_input.disable()

        @aug_category_selector.value_changed
        def aug_category_selector_cb(value):
            new_funcs = augs_json.get(value)
            aug_func_selector.set([Select.Item(new_func) for new_func in new_funcs.keys()])

        @aug_func_selector.value_changed
        def aug_func_selector_cb(value):
            nonlocal fields_container

            fields_container = Container(
                _get_params_widget(aug_category_selector.get_value(), value)
            )
            aug_params_field._content = fields_container

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="Sidebar",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=pipeline_layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            Container([pipeline_sidebar_field, aug_add_field])
                        ),
                        sidebar_width=420,
                    ),
                ),
                # NodesFlow.Node.Option(
                #     name="Pipeline",
                #     option_component=NodesFlow.WidgetOptionComponent(
                #         aug_add_field,
                #         sidebar_component=NodesFlow.WidgetOptionComponent(aug_add_field),
                #         sidebar_width=420,
                #     ),
                # ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=False,
        )

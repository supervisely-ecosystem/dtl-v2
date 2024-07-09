from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


from supervisely.app.widgets import (
    NodesFlow,
    Select,
)

from supervisely.app.content import StateJson, DataJson


from src.ui.dtl import ImgAugAugmentationsAction
from src.ui.widgets.augs_list import AugsList
from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_sidebar import (
    create_sidebar_widgets,
    augs_json,
    _get_params_widget,
)

from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_layout import create_layout_widgets


class ImgAugStudioAction(ImgAugAugmentationsAction):
    name = "imgaug_studio"
    title = "ImgAug Studio"
    docs_url = ""
    description = "ImgAug Studio app in a node format."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        saved_settings = {"pipeline": {}}

        layout_text, layout_edit_button, layout_container = create_layout_widgets()

        (
            # Sidebar Aug category widgets
            sidebar_category_items,
            sidebar_category_selector,
            sidebar_category_field,
            # Sidebar Aug method widgets
            sidebar_method_list,
            sidebar_method_items,
            sidebar_method_selector,
            sidebar_method_field,
            # Sidebar Aug probability widgets
            sidebar_sometimes_check,
            sidebar_sometimes_input,
            sidebar_sometimes_container,
            sidebar_sometimes_field,
            # Sidebar Aug params widgets
            sidebar_params_widgets,
            sidebar_params_container,
            sidebar_params_field,
            # Sidebar add Aug
            sidebar_add_to_pipeline_button,
            sidebar_add_container,
            # Sidebar layout widgets
            sidebar_layout_pipeline,
            sidebar_layout_add_aug_button,
            sidebar_layout_aug_add_field,
            pipeline_sidebar_container,
        ) = create_sidebar_widgets()
        sidebar_layout_aug_add_field.hide()

        @sidebar_add_to_pipeline_button.click
        def sidebar_add_to_pipeline_button_cb():
            category = sidebar_category_selector.get_value()
            method = sidebar_method_selector.get_value()
            params = [field for field in sidebar_params_widgets]  # todo
            if sidebar_sometimes_check.is_checked():
                sometimes = sidebar_sometimes_input.get_value()
            else:
                sometimes = None
            sidebar_params_widgets.append(AugsList.AugItem(category, method, params, sometimes))
            saved_settings["pipeline"] = sidebar_params_widgets.get_pipeline()
            sidebar_layout_aug_add_field.hide()
            sidebar_layout_add_aug_button.enable()

        @sidebar_layout_add_aug_button.click
        def sidebar_add_aug_button_cb():
            sidebar_layout_aug_add_field.show()
            sidebar_layout_add_aug_button.disable()

        @sidebar_sometimes_check.value_changed
        def sidebar_sometimes_check_cb(is_checked):
            if is_checked:
                sidebar_sometimes_input.enable()
            else:
                sidebar_sometimes_input.disable()

        @sidebar_category_selector.value_changed
        def sidebar_category_selector_cb(current_category):
            current_category_methods = augs_json.get(current_category)
            sidebar_method_selector.set(
                [Select.Item(new_func) for new_func in current_category_methods]
            )

        @sidebar_method_selector.value_changed
        def sidebar_method_selector_cb(current_method):
            current_category = sidebar_category_selector.get_value()
            current_param_widgets = _get_params_widget(current_category, current_method)

            sidebar_params_container._widgets = current_param_widgets
            sidebar_params_field._content = sidebar_params_container
            StateJson().update()
            DataJson().update()

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="Layout",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            pipeline_sidebar_container
                        ),
                        sidebar_width=420,
                    ),
                )
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


# @TODO: create one widget of each param type, hide, show, change values based on the selected method

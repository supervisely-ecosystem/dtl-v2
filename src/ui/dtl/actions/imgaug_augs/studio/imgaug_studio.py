from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


from supervisely.app.widgets import (
    NodesFlow,
    Select,
)

from src.ui.dtl import ImgAugAugmentationsAction
from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_sidebar import (
    create_sidebar_widgets,
)

from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_layout import create_layout_widgets
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as aug_utils


class ImgAugStudioAction(ImgAugAugmentationsAction):
    name = "imgaug_studio"
    title = "ImgAug Studio"
    docs_url = ""
    description = "ImgAug Studio app in a node format."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        saved_settings = {
            "pipeline": [],
            "shuffle": False,
        }

        (
            # Layout
            layout_text,
            layout_edit_button,
            layout_container,
            # Preview
            layout_pipeline_preview,
            layout_shuffle_preview,
            layout_preview_container,
        ) = create_layout_widgets()

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
            sidebar_params_reloadable,
            sidebar_params_field,
            # Sidebar add Aug
            sidebar_add_to_pipeline_button,
            sidebar_cancel_add_to_pipeline_button,
            sidebar_add_container,
            # Sidebar layout widgets
            sidebar_layout_pipeline,
            sidebar_layout_add_aug_button,
            sidebar_layout_aug_add_field,
            sidebar_layout_save_btn,
            sidebar_layout_buttons_container,
            pipeline_sidebar_container,
        ) = create_sidebar_widgets()
        sidebar_layout_aug_add_field.hide()

        @sidebar_add_to_pipeline_button.click
        def sidebar_add_to_pipeline_button_cb():
            category = sidebar_category_selector.get_value()
            method = sidebar_method_selector.get_value()
            params = aug_utils.get_params_from_widgets(sidebar_params_widgets)
            if sidebar_sometimes_check.is_checked():
                sometimes = sidebar_sometimes_input.get_value()
            else:
                sometimes = None
            sidebar_layout_pipeline.append_aug(category, method, params, sometimes)
            sidebar_layout_aug_add_field.hide()
            sidebar_layout_add_aug_button.enable()
            sidebar_layout_save_btn.enable()

        @sidebar_cancel_add_to_pipeline_button.click
        def sidebar_cancel_add_to_pipeline_button_cb():
            sidebar_layout_aug_add_field.hide()
            sidebar_layout_add_aug_button.enable()
            sidebar_layout_save_btn.enable()

        @sidebar_layout_save_btn.click
        def sidebar_layout_save_btn_cb():
            nonlocal saved_settings
            pipeline = sidebar_layout_pipeline.get_pipeline()
            shuffle = sidebar_layout_pipeline.is_shuffled()

            layout_pipeline_preview.set(pipeline)
            layout_shuffle_preview.set(f"Randomize order: {shuffle}", "text")
            saved_settings = {
                "pipeline": pipeline,
                "shuffle": shuffle,
            }

        @sidebar_layout_add_aug_button.click
        def sidebar_add_aug_button_cb():
            sidebar_category_selector.set_value("arithmetic")
            sidebar_method_selector.set_value("Add")
            sidebar_layout_aug_add_field.show()
            sidebar_layout_add_aug_button.disable()
            sidebar_layout_save_btn.disable()

        @sidebar_sometimes_check.value_changed
        def sidebar_sometimes_check_cb(is_checked):
            if is_checked:
                sidebar_sometimes_input.enable()
            else:
                sidebar_sometimes_input.disable()

        @sidebar_category_selector.value_changed
        def sidebar_category_selector_cb(current_category):
            current_category_methods = aug_utils.augs_json.get(current_category)
            sidebar_method_selector.set(
                [Select.Item(new_func) for new_func in current_category_methods]
            )

        @sidebar_method_selector.value_changed
        def sidebar_method_selector_cb(current_method):
            nonlocal sidebar_params_widgets, sidebar_params_container, sidebar_params_reloadable
            current_category = sidebar_category_selector.get_value()
            sidebar_params_widgets = aug_utils.get_params_widget(current_category, current_method)

            sidebar_params_container._widgets = sidebar_params_widgets
            sidebar_params_reloadable.set_content(sidebar_params_container)
            sidebar_params_reloadable.reload()

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
                        sidebar_width=680,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Layout Preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=layout_preview_container
                    ),
                ),
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
            need_preview=True,
        )


# @TODO: value previews for slider (like in app) - slider - (-4.50, 3.30)
# @TODO: add batch processing to compute

# @TODO: [LOW PRIORITY] create one widget of each param type, hide, show, change values based on the selected method (? use reloadable for now)

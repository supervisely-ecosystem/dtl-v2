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
from supervisely.api.file_api import FileApi
import src.globals as g


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
            # Sidebar Initialization widgets
            sidebar_init_selector,
            # sidebar_init_new_button,
            # sidebar_init_selector_container,
            sidebar_init_input,
            sidebar_init_input_button,
            sidebar_init_input_container,
            sidebar_init_input_filethumb,
            sidebar_init_container,
            sidebar_init_field,
            # Sidebar create Aug
            sidebar_params_widget,
            sidebar_add_to_pipeline_button,
            sidebar_cancel_add_to_pipeline_button,
            sidebar_add_container,
            # Sidebar layout widgets
            sidebar_layout_pipeline,
            sidebar_layout_add_aug_button,
            sidebar_layout_save_btn,
            sidebar_layout_buttons_container,
            pipeline_sidebar_container,
        ) = create_sidebar_widgets()

        @sidebar_add_to_pipeline_button.click
        def sidebar_add_to_pipeline_button_cb():
            category = sidebar_params_widget.get_category()
            method = sidebar_params_widget.get_method()
            params = sidebar_params_widget.get_params()
            sometimes = sidebar_params_widget.get_probability()

            # sidebar_layout_pipeline.append_aug(**aug_info)
            sidebar_layout_pipeline.append_aug(category, method, params, sometimes)

            sidebar_add_container.hide()
            sidebar_layout_add_aug_button.enable()
            sidebar_layout_save_btn.enable()

        @sidebar_cancel_add_to_pipeline_button.click
        def sidebar_cancel_add_to_pipeline_button_cb():
            sidebar_add_container.hide()
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
            sidebar_add_container.show()
            sidebar_layout_add_aug_button.disable()
            sidebar_layout_save_btn.disable()

        @sidebar_init_selector.value_changed
        def sidebar_init_selecor_cb(value):
            if value == 0:
                sidebar_init_input_container.hide()
                sidebar_layout_pipeline.show()
                sidebar_layout_buttons_container.show()
            elif value == 1:
                sidebar_init_input_container.show()
                sidebar_layout_pipeline.hide()
                sidebar_layout_buttons_container.hide()

        @sidebar_init_input.value_changed
        def sidebar_init_input_cb(value):
            file_info = None
            if len(value) > 0 and value != "":
                sidebar_init_input_filethumb.show()
                file_info = FileApi(g.api).get_info_by_path(g.TEAM_ID, value)
            else:
                sidebar_init_input_filethumb.hide()

            sidebar_init_input_filethumb.set(file_info)
            if file_info is not None:
                sidebar_init_input_button.enable()
            else:
                sidebar_init_input_button.disable()

        @sidebar_init_input_button.click
        def sidebar_init_input_button_cb():
            sidebar_init_input.disable()
            sidebar_init_input_button.disable()
            file_info = sidebar_init_input_filethumb.get_json_data()
            pipeline = aug_utils.get_pipeline_from_fileinfo(file_info)
            sidebar_layout_pipeline.set_pipeline(pipeline)
            sidebar_layout_pipeline.show()
            sidebar_layout_buttons_container.show()

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

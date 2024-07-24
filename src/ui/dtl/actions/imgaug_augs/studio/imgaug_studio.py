from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

from supervisely import ProjectMeta, Polygon
from supervisely.app.widgets import NodesFlow

from src.ui.dtl import ImgAugAugmentationsAction
from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_sidebar import (
    create_sidebar_widgets,
)
from src.ui.dtl.utils import classes_list_to_mapping

from src.ui.dtl.actions.imgaug_augs.studio.layout.imgaug_studio_layout import create_layout_widgets
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as aug_utils
import src.globals as g


class ImgAugStudioAction(ImgAugAugmentationsAction):
    name = "imgaug_studio"
    title = "ImgAug Studio"
    docs_url = ""
    description = "ImgAug Studio app in a node format."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        custom_pipeline_file_info = []
        _current_meta = ProjectMeta()
        classes_to_convert = classes_list_to_mapping(
            [], [oc.name for oc in _current_meta.obj_classes], other="skip"
        )

        saved_settings = {
            "pipeline": [],
            "shuffle": False,
            "classes_to_convert": classes_to_convert,
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
            sidebar_team_files_link_btn,
            sidebar_init_input,
            sidebar_init_load_button,
            sidebar_init_input_container,
            sidebar_init_input_filethumb,
            sidebar_init_warning_text,
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
            sidebar_layout_reset_aug_button,
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
            sidebar_layout_pipeline.append_aug(category, method, params, sometimes)

            sidebar_add_container.hide()
            sidebar_init_selector.enable()
            sidebar_layout_add_aug_button.enable()
            sidebar_layout_reset_aug_button.enable()
            sidebar_layout_save_btn.enable()

        @sidebar_layout_reset_aug_button.click
        def sidebar_reset_aug_button_cb():
            sidebar_layout_pipeline.set_pipeline([])
            sidebar_init_input.set_value("")
            sidebar_init_input_filethumb.set(None)
            sidebar_init_load_button.enable()
            sidebar_init_input.enable()

        @sidebar_cancel_add_to_pipeline_button.click
        def sidebar_cancel_add_to_pipeline_button_cb():
            sidebar_add_container.hide()
            sidebar_init_selector.enable()
            sidebar_layout_add_aug_button.enable()
            sidebar_layout_reset_aug_button.enable()
            sidebar_layout_save_btn.enable()

        @sidebar_layout_save_btn.click
        def sidebar_layout_save_btn_cb():
            nonlocal saved_settings, classes_to_convert
            pipeline = sidebar_layout_pipeline.get_pipeline()
            shuffle = sidebar_layout_pipeline.is_shuffled()
            saved_settings = {
                "pipeline": pipeline,
                "shuffle": shuffle,
                "classes_to_convert": classes_to_convert,
            }
            layout_pipeline_preview.set(pipeline)
            layout_shuffle_preview.set(f"Randomize order: {shuffle}", "text")
            g.updater(("nodes", layer_id))

        @sidebar_layout_add_aug_button.click
        def sidebar_add_aug_button_cb():
            sidebar_add_container.show()
            sidebar_init_selector.disable()
            sidebar_layout_add_aug_button.disable()
            sidebar_layout_reset_aug_button.disable()
            sidebar_layout_save_btn.disable()

        @sidebar_init_selector.value_changed
        def sidebar_init_selector_cb(value):
            if value == 0:
                sidebar_team_files_link_btn.hide()
                sidebar_init_input_container.hide()
            elif value == 1:
                sidebar_init_input_container.show()
                sidebar_team_files_link_btn.show()

        @sidebar_init_input.value_changed
        def sidebar_init_input_cb(path_to_pipeline):
            nonlocal custom_pipeline_file_info
            sidebar_init_warning_text.hide()
            custom_pipeline_file_info = None
            if len(path_to_pipeline) > 0 and path_to_pipeline != "":
                sidebar_init_input_filethumb.show()
                custom_pipeline_file_info = g.api.file.get_info_by_path(g.TEAM_ID, path_to_pipeline)
            else:
                sidebar_init_input_filethumb.hide()

            sidebar_init_input_filethumb.set(custom_pipeline_file_info)
            if custom_pipeline_file_info is not None:
                if custom_pipeline_file_info.ext == "json":
                    sidebar_init_load_button.enable()
                else:
                    sidebar_init_warning_text.set(
                        "Invalid file format. Please select a JSON file.", "error"
                    )
                    sidebar_init_warning_text.show()
            else:
                sidebar_init_load_button.disable()

        @sidebar_init_load_button.click
        def sidebar_init_load_button_cb():
            nonlocal custom_pipeline_file_info
            sidebar_init_input.disable()
            sidebar_init_load_button.disable()
            pipeline = aug_utils.get_pipeline_from_fileinfo(
                custom_pipeline_file_info, sidebar_init_warning_text
            )
            sidebar_layout_pipeline.set_pipeline(pipeline)
            sidebar_layout_pipeline.show()
            sidebar_layout_buttons_container.show()

        def data_changed_cb(**kwargs):
            project_meta = kwargs.get("project_meta", None)
            if project_meta is None:
                return

            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            # update settings according to new meta
            nonlocal saved_settings, classes_to_convert
            obj_classes = [cls for cls in project_meta.obj_classes if cls.geometry_type is Polygon]
            classes_to_convert = {obj_class.name: obj_class.name for obj_class in obj_classes}

            classes_to_convert = classes_list_to_mapping(
                classes_to_convert, [oc.name for oc in _current_meta.obj_classes], other="skip"
            )
            saved_settings["classes_to_convert"] = classes_to_convert

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def _set_settings_from_json(settings: dict):
            nonlocal saved_settings
            pipeline_json = settings.get("pipeline", [])
            shuffle = settings.get("shuffle", False)
            sidebar_layout_pipeline.from_json(pipeline_json, shuffle)
            saved_settings = {
                "pipeline": pipeline_json,
                "shuffle": shuffle,
                "classes_to_convert": classes_to_convert,
            }
            layout_pipeline_preview.set(pipeline_json)
            layout_shuffle_preview.set(f"Randomize order: {shuffle}", "text")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
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
            data_changed_cb=data_changed_cb,
            need_preview=True,
        )

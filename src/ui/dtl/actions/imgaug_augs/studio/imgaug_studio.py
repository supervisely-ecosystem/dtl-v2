from typing import Optional
from os.path import realpath, dirname
from supervisely import logger
from supervisely.nn.inference.session import Session

from src.ui.dtl.Layer import Layer

from src.ui.dtl.actions.imgaug_augs.studio.layout.node_layout import create_node_layout
from src.ui.dtl.actions.imgaug_augs.studio.layout.pipeline import create_pipeline_widgets
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as utils
import src.globals as g


class ImgAugStudioAction(Layer):
    name = "imgaug_studio_action"
    title = "ImgAug Studio"
    description = ""
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
        (
            pipeline_layout_text,
            pipeline_layout_edit_button,
            pipeline_layout_container,
            pipeline_widget,
            add_button,
            preview_button,
            export_button,
            actions_container,
            pipeline_sidebar_container,
            pipeline_sidebar_field,
        ) = create_pipeline_widgets()

        @pipeline_layout_edit_button.click
        def pipeline_layout_edit_button_cb():
            pipeline_widget.show()
            NotImplemented

        @add_button.click
        def add_button_cb(category, method, params):
            pipeline_widget.append(AugItem(category=category, method=method, params=params))
            NotImplemented

        @preview_button.click
        def preview_button_cb(context, state):
            utils.preview_pipeline(g.api, g.api.task_id, context, state)
            NotImplemented
        
        @export_button.click
        def export_button_cb():
            utils.

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

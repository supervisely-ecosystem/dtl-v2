from typing import Optional
from os.path import realpath, dirname
from supervisely.app.widgets import NodesFlow, Input, Text

from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size


class DeployYOLOV8Action(NeuralNetworkAction):
    name = "deploy_yolov8"
    title = "Deploy YoloV8"
    docs_url = ""
    description = "Deploy YoloV8 models."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {}

        def _set_settings_from_json(settings: dict):
            pass

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="class_text",
                    option_component=NodesFlow.WidgetOptionComponent(bg_class_name_text),
                ),
                NodesFlow.Node.Option(
                    name="class",
                    option_component=NodesFlow.WidgetOptionComponent(bg_class_name_input),
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
            need_preview=False,
        )

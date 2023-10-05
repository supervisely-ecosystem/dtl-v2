from typing import Optional
from os.path import realpath, dirname
from supervisely.app.widgets import NodesFlow

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

class BackgroundAction(AnnotationAction):
    name = "background"
    title = "Background"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/background"
    )
    description = "Use to prepare data to train Neural Network for semantic segmentation."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "class": options_json["class"] if options_json["class"] else "",
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            class_val = settings.get("class", "")
            settings_options = [
                NodesFlow.Node.Option(
                    name="class_text",
                    option_component=NodesFlow.TextOptionComponent("Background Class name"),
                ),
                NodesFlow.Node.Option(
                    name="class", option_component=NodesFlow.InputOptionComponent(class_val)
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
        )

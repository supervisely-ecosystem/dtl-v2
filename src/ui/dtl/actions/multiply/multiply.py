from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class MultiplyAction(SpatialLevelAction):
    name = "multiply"
    title = "Multiply"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/multiply"
    description = "Duplicates data (image + annotation)."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "multiply": options_json["multiply"],
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            multiply_val = settings.get("multiply", 1)
            settings_options = [
                NodesFlow.Node.Option(
                    name="multiply_text",
                    option_component=NodesFlow.TextOptionComponent("Multiply number"),
                ),
                NodesFlow.Node.Option(
                    name="multiply",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=1, default_value=multiply_val
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
        )

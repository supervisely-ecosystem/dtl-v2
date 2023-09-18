from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer


class MultiplyAction(SpatialLevelAction):
    name = "multiply"
    title = "Multiply"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/multiply"
    description = "This layer (multiply) duplicates data (image + annotation)."

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

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

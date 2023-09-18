from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer


class RandomColorsAction(AnnotationAction):
    name = "random_color"
    title = "Random Color"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/random_color"
    )
    description = (
        "This layer (random_color) changes image colors by random moving each of RGB components."
    )

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
                "strength": options_json["strength"],
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            str_val = settings.get("strength", 0.25)
            settings_options = [
                NodesFlow.Node.Option(
                    name="strength_text",
                    option_component=NodesFlow.TextOptionComponent("Strength"),
                ),
                NodesFlow.Node.Option(
                    name="strength",
                    option_component=NodesFlow.SliderOptionComponent(
                        min=0, max=1, default_value=str_val
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

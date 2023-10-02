from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import PixelLevelAction
from src.ui.dtl.Layer import Layer


class NoiseAction(PixelLevelAction):
    name = "noise"
    title = "Noise"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/noise"
    description = "Noise layer (noise) adds noise of Gaussian distribution to the images."

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
                "mean": options_json["mean"],
                "std": options_json["std"],
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            mean_val = settings.get("mean", 10)
            std_val = settings.get("std", 50)
            settings_options = [
                NodesFlow.Node.Option(
                    name="mean_text",
                    option_component=NodesFlow.TextOptionComponent("Mean"),
                ),
                NodesFlow.Node.Option(
                    name="mean",
                    option_component=NodesFlow.NumberOptionComponent(default_value=mean_val),
                ),
                NodesFlow.Node.Option(
                    name="std_text",
                    option_component=NodesFlow.TextOptionComponent("Spread"),
                ),
                NodesFlow.Node.Option(
                    name="std",
                    option_component=NodesFlow.NumberOptionComponent(default_value=std_val),
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

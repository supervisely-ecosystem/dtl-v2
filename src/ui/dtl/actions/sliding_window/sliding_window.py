from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer


class SlidingWindowAction(SpatialLevelAction):
    name = "sliding_window"
    title = "Sliding Window"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/sliding_window"
    )
    description = "This layer (sliding_window) is used to crop part of image with its annotations by sliding of window from left to rigth, from top to bottom."

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
                "window": {
                    "width": options_json["window_width"],
                    "height": options_json["window_height"],
                },
                "min_overlap": {
                    "x": options_json["min_overlap_x"],
                    "y": options_json["min_overlap_y"],
                },
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            width_val = settings.get("window", {}).get("width", 128)
            height_val = settings.get("window", {}).get("height", 128)
            min_overlap_x_val = settings.get("min_overlap", {}).get("x", 32)
            min_overlap_y_val = settings.get("min_overlap", {}).get("y", 32)
            settings_options = [
                NodesFlow.Node.Option(
                    name="window_text",
                    option_component=NodesFlow.TextOptionComponent("Window"),
                ),
                NodesFlow.Node.Option(
                    name="window_width_text",
                    option_component=NodesFlow.TextOptionComponent("Width"),
                ),
                NodesFlow.Node.Option(
                    name="window_width",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=1, default_value=width_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="window_height_text",
                    option_component=NodesFlow.TextOptionComponent("Height"),
                ),
                NodesFlow.Node.Option(
                    name="window_height",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=1, default_value=height_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="min_overlap_text",
                    option_component=NodesFlow.TextOptionComponent("Min Overlap"),
                ),
                NodesFlow.Node.Option(
                    name="min_overlap_x_text",
                    option_component=NodesFlow.TextOptionComponent("X"),
                ),
                NodesFlow.Node.Option(
                    name="min_overlap_x",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=1, default_value=min_overlap_x_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="min_overlap_y_text",
                    option_component=NodesFlow.TextOptionComponent("Y"),
                ),
                NodesFlow.Node.Option(
                    name="min_overlap_y",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=1, default_value=min_overlap_y_val
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

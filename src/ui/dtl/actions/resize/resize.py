from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer


class ResizeAction(SpatialLevelAction):
    name = "resize"
    title = "Resize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/resize"
    description = "Resize layer (resize) resizes data (image + annotation) to the certain size."

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            keep_aspect_ratio = bool(options_json["Keep aspect ratio"])
            width = options_json["width"]
            height = options_json["height"]
            if width * height == 0:
                raise ValueError("Width and Height must be positive")
            if not keep_aspect_ratio:
                if width == -1:
                    raise ValueError(
                        "Width = -1 is not allowed when Keep aspect ratio is not enabled"
                    )
                if height == -1:
                    raise ValueError(
                        "Height = -1 is not allowed when Keep aspect ratio is not enabled"
                    )
            return {
                "width": width,
                "height": height,
                "aspect_ratio": {
                    "keep": keep_aspect_ratio,
                },
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            width_val = settings.get("width", 1)
            height_val = settings.get("height", 1)
            keep_aspect_ratio = settings.get("aspect_ratio", {}).get("keep", False)
            settings_options = [
                NodesFlow.Node.Option(
                    name="width_text",
                    option_component=NodesFlow.TextOptionComponent("Width"),
                ),
                NodesFlow.Node.Option(
                    name="width",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=-1, default_value=width_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="height_text",
                    option_component=NodesFlow.TextOptionComponent("Height"),
                ),
                NodesFlow.Node.Option(
                    name="height",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=-1, default_value=height_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Keep aspect ratio",
                    option_component=NodesFlow.CheckboxOptionComponent(
                        default_value=keep_aspect_ratio
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

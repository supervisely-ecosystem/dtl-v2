from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow, InputNumber, Text, Checkbox

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class ResizeAction(SpatialLevelAction):
    name = "resize"
    title = "Resize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/resize"
    description = "Resize data (image + annotation) to the certain size."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        width_text = Text("Width", status="text")
        width_input = InputNumber(value=3, step=1, controls=True)

        height_text = Text("Height", status="text")
        height_input = InputNumber(value=3, step=1, controls=True)

        keep_aspect_ratio_checkbox = Checkbox("Keep aspect ratio")

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            keep_aspect_ratio = keep_aspect_ratio_checkbox.is_checked()
            width = width_input.get_value()
            height = height_input.get_value()
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
            settings_options = [
                NodesFlow.Node.Option(
                    name="width_text",
                    option_component=NodesFlow.WidgetOptionComponent(width_text),
                ),
                NodesFlow.Node.Option(
                    name="width_input",
                    option_component=NodesFlow.WidgetOptionComponent(width_input),
                ),
                NodesFlow.Node.Option(
                    name="height_text",
                    option_component=NodesFlow.WidgetOptionComponent(height_text),
                ),
                NodesFlow.Node.Option(
                    name="height_input",
                    option_component=NodesFlow.WidgetOptionComponent(height_input),
                ),
                NodesFlow.Node.Option(
                    name="keep_aspect_ratio_checkbox",
                    option_component=NodesFlow.WidgetOptionComponent(keep_aspect_ratio_checkbox),
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

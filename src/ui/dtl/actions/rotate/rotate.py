from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow, InputNumber, Text, Select

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class RotateAction(SpatialLevelAction):
    name = "rotate"
    title = "Rotate"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/rotate"
    description = "Rotate images and it's annotations."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        rotate_angles_text = Text("Rotate Angles", status="text")

        min_degrees_text = Text("Min degrees", status="text")
        min_degrees_input = InputNumber(value=45, step=1, controls=True)

        max_degrees_text = Text("Max degrees", status="text")
        max_degrees_input = InputNumber(value=45, step=1, controls=True)

        br_text = Text("Black Regions", status="text")
        br_selector_items = [
            Select.Item("keep", "Keep"),
            Select.Item("crop", "Crop"),
            Select.Item("preserve_size", "Preserve Size"),
        ]
        br_selector = Select(items=br_selector_items, size="small")

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "rotate_angles": {
                    "min_degrees": min_degrees_input.get_value(),
                    "max_degrees": max_degrees_input.get_value(),
                },
                "black_regions": {"mode": br_selector.get_value()},
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="rotate_angles_text",
                    option_component=NodesFlow.WidgetOptionComponent(rotate_angles_text),
                ),
                NodesFlow.Node.Option(
                    name="min_degrees_text",
                    option_component=NodesFlow.WidgetOptionComponent(min_degrees_text),
                ),
                NodesFlow.Node.Option(
                    name="min_degrees",
                    option_component=NodesFlow.WidgetOptionComponent(min_degrees_input),
                ),
                NodesFlow.Node.Option(
                    name="max_degrees_text",
                    option_component=NodesFlow.WidgetOptionComponent(max_degrees_text),
                ),
                NodesFlow.Node.Option(
                    name="max_degrees",
                    option_component=NodesFlow.WidgetOptionComponent(max_degrees_input),
                ),
                NodesFlow.Node.Option(
                    name="black_regions_text",
                    option_component=NodesFlow.WidgetOptionComponent(br_text),
                ),
                NodesFlow.Node.Option(
                    name="black_regions",
                    option_component=NodesFlow.WidgetOptionComponent(br_selector),
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

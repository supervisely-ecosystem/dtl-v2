from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow, InputNumber, Text

from src.ui.dtl import PixelLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class NoiseAction(PixelLevelAction):
    name = "noise"
    title = "Noise"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/noise"
    description = "Add gaussian noise to the images."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        mean_text = Text("Mean")
        mean_input = InputNumber(value=10.000, step=0.1, precision=3, controls=True)

        spread_text = Text("Spread")
        spread_input = InputNumber(value=50.000, step=0.1, controls=True)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "mean": mean_input.get_value(),
                "std": spread_input.get_value(),
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            mean_val = settings.get("mean", 10)
            std_val = settings.get("std", 50)
            settings_options = [
                NodesFlow.Node.Option(
                    name="mean_text",
                    option_component=NodesFlow.WidgetOptionComponent(mean_text),
                ),
                NodesFlow.Node.Option(
                    name="mean",
                    option_component=NodesFlow.WidgetOptionComponent(mean_input),
                ),
                NodesFlow.Node.Option(
                    name="std_text",
                    option_component=NodesFlow.WidgetOptionComponent(spread_text),
                ),
                NodesFlow.Node.Option(
                    name="std",
                    option_component=NodesFlow.WidgetOptionComponent(spread_input),
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

from typing import Optional

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

class FlipAction(SpatialLevelAction):
    name = "flip"
    title = "Flip"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/flip"
    description = "Flips data (image + annotation) vertically or horizontally."
    md_description = get_layer_docs()

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "axis": options_json["axis"],
            }

        axis_option_items = [
            NodesFlow.SelectOptionComponent.Item("vertical", "Vertical"),
            NodesFlow.SelectOptionComponent.Item("horizontal", "Horizontal"),
        ]

        def create_options(src: list, dst: list, settings: dict) -> dict:
            axis_val = settings.get("axis", "vertical")
            settings_options = [
                NodesFlow.Node.Option(
                    name="axis_text",
                    option_component=NodesFlow.TextOptionComponent("Axis"),
                ),
                NodesFlow.Node.Option(
                    name="axis",
                    option_component=NodesFlow.SelectOptionComponent(
                        axis_option_items, default_value=axis_val
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

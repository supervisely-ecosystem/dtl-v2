from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class SlidingWindowAction(Action):
    name = "sliding_window"
    title = "Sliding Window"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/sliding_window"
    )
    description = "This layer (sliding_window) is used to crop part of image with its annotations by sliding of window from left to rigth, from top to bottom."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "window": None,
        "min_overlap": None,
    }

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

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            node_state["window_width"] = settings["window"]["width"]
            node_state["window_height"] = settings["window"]["height"]
            node_state["min_overlap_x"] = settings["min_overlap"]["x"]
            node_state["min_overlap_y"] = settings["min_overlap"]["y"]
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
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
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=128),
            ),
            NodesFlow.Node.Option(
                name="window_height_text",
                option_component=NodesFlow.TextOptionComponent("Height"),
            ),
            NodesFlow.Node.Option(
                name="window_height",
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=128),
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
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=32),
            ),
            NodesFlow.Node.Option(
                name="min_overlap_y_text",
                option_component=NodesFlow.TextOptionComponent("Y"),
            ),
            NodesFlow.Node.Option(
                name="min_overlap_y",
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=32),
            ),
        ]

        return Layer(
            action=cls,
            id=layer_id,
            options=options,
            get_src=None,
            get_dst=None,
            get_settings=get_settings,
            meta_changed_cb=None,
            set_settings_from_json=set_settings_from_json,
        )

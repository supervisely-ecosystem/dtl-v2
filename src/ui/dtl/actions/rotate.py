from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class RotateAction(Action):
    name = "rotate"
    title = "Rotate"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/rotate"
    description = "Rotate layer (rotate) rotates images and its annotations."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "rotate_angles": None,
        "black_regions": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "rotate_angles": {
                    "min_degrees": options_json["min_degrees"],
                    "max_degrees": options_json["max_degrees"],
                },
                "black_regions": {"mode": options_json["black_regions"]},
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            node_state["min_degrees"] = settings["rotate_angles"]["min_degrees"]
            node_state["max_degrees"] = settings["rotate_angles"]["max_degrees"]
            node_state["black_regions"] = settings["black_regions"]["mode"]
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="rotate_angles_text",
                option_component=NodesFlow.TextOptionComponent("Rotate Angles"),
            ),
            NodesFlow.Node.Option(
                name="min_degrees_text",
                option_component=NodesFlow.TextOptionComponent("Min Degrees"),
            ),
            NodesFlow.Node.Option(
                name="min_degrees",
                option_component=NodesFlow.IntegerOptionComponent(default_value=45),
            ),
            NodesFlow.Node.Option(
                name="max_degrees_text",
                option_component=NodesFlow.TextOptionComponent("Max Degrees"),
            ),
            NodesFlow.Node.Option(
                name="max_degrees",
                option_component=NodesFlow.IntegerOptionComponent(default_value=45),
            ),
            NodesFlow.Node.Option(
                name="black_regions_text",
                option_component=NodesFlow.TextOptionComponent("Black Regions"),
            ),
            NodesFlow.Node.Option(
                name="black_regions",
                option_component=NodesFlow.SelectOptionComponent(
                    items=[
                        NodesFlow.SelectOptionComponent.Item("keep", "Keep"),
                        NodesFlow.SelectOptionComponent.Item("crop", "Crop"),
                        NodesFlow.SelectOptionComponent.Item("preserve_size", "Preserve Size"),
                    ]
                ),
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

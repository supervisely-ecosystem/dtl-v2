from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class ResizeAction(Action):
    name = "resize"
    title = "Resize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/resize"
    description = "Resize layer (resize) resizes data (image + annotation) to the certain size."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "aspect_ratio": None,
    }

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

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            node_state["Keep aspect ratio"] = settings["aspect_ratio"]["keep"]
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="width_text",
                option_component=NodesFlow.TextOptionComponent("Width"),
            ),
            NodesFlow.Node.Option(
                name="width",
                option_component=NodesFlow.IntegerOptionComponent(min=-1, default_value=1),
            ),
            NodesFlow.Node.Option(
                name="height_text",
                option_component=NodesFlow.TextOptionComponent("Height"),
            ),
            NodesFlow.Node.Option(
                name="height",
                option_component=NodesFlow.IntegerOptionComponent(min=-1, default_value=1),
            ),
            NodesFlow.Node.Option(
                name="Keep aspect ratio",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=False),
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

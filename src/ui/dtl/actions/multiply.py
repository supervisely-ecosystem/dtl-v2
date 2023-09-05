from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class MultiplyAction(Action):
    name = "multiply"
    title = "Multiply"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/multiply"
    description = "This layer (multiply) duplicates data (image + annotation)."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {}

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "multiply": options_json["multiply"],
            }

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="multiply_text",
                option_component=NodesFlow.TextOptionComponent("Multiply number"),
            ),
            NodesFlow.Node.Option(
                name="multiply",
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=1),
            ),
        ]
        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=None,
            set_settings_from_json=None,
            id=layer_id,
        )

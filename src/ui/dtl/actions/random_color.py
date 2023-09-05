from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class RandomColorsAction(Action):
    name = "random_color"
    title = "Random Color"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/random_color"
    )
    description = (
        "This layer (random_color) changes image colors by random moving each of RGB components."
    )
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
                "strength": options_json["strength"],
            }

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="strength_text",
                option_component=NodesFlow.TextOptionComponent("Strength"),
            ),
            NodesFlow.Node.Option(
                name="strength",
                option_component=NodesFlow.SliderOptionComponent(min=0, max=1, default_value=0.25),
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

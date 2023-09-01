from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class NoiseAction(Action):
    name = "noise"
    title = "Noise"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/noise"
    description = "Noise layer (noise) adds noise of Gaussian distribution to the images."
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
                "mean": options_json["mean"],
                "std": options_json["std"],
            }

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="mean_text",
                option_component=NodesFlow.TextOptionComponent("Mean"),
            ),
            NodesFlow.Node.Option(
                name="mean",
                option_component=NodesFlow.NumberOptionComponent(default_value=10),
            ),
            NodesFlow.Node.Option(
                name="std_text",
                option_component=NodesFlow.TextOptionComponent("Spread"),
            ),
            NodesFlow.Node.Option(
                name="std",
                option_component=NodesFlow.NumberOptionComponent(default_value=50),
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

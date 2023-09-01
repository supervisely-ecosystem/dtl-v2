from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class ContrastBrightnessAction(Action):
    name = "contrast_brightness"
    title = "Contrast / Brightness"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/contrast_brightness"
    description = (
        "This layer (contrast_brightness) randomly changes contrast and brightness of images. "
    )
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "contrast": None,
        "brightness": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            settings = {}
            if options_json["Contrast"]:
                settings["contrast"] = {
                    "min": options_json["Contrast Min"],
                    "max": options_json["Contrast Max"],
                    "center_grey": options_json["Center grey"]
                    if options_json["Center grey"]
                    else False,
                }
            else:
                settings["contrast"] = {
                    "min": 1,
                    "max": 1,
                    "center_grey": False,
                }
            if options_json["Brightness"]:
                settings["brightness"] = {
                    "min": options_json["Brightness Min"],
                    "max": options_json["Brightness Max"],
                }
            else:
                settings["brightness"] = {
                    "min": 0,
                    "max": 0,
                }
            return settings

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            if "contrast" in settings:
                node_state["Contrast"] = True
                node_state["Contrast Min"] = settings["contrast"]["min"]
                node_state["Contrast Max"] = settings["contrast"]["max"]
                node_state["Center grey"] = settings["contrast"]["center_grey"]
            if "brightness" in settings:
                node_state["Brightness"] = True
                node_state["Brightness Min"] = settings["brightness"]["min"]
                node_state["Brightness Max"] = settings["brightness"]["max"]
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="Contrast",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=True),
            ),
            NodesFlow.Node.Option(
                name="Contrast Min",
                option_component=NodesFlow.NumberOptionComponent(min=0, max=10, default_value=1),
            ),
            NodesFlow.Node.Option(
                name="Contrast Max",
                option_component=NodesFlow.NumberOptionComponent(min=0, max=10, default_value=2),
            ),
            NodesFlow.Node.Option(
                name="Center grey",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=False),
            ),
            NodesFlow.Node.Option(
                name="Brightness",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=True),
            ),
            NodesFlow.Node.Option(
                name="Brightness Min",
                option_component=NodesFlow.NumberOptionComponent(
                    min=-255, max=255, default_value=-50
                ),
            ),
            NodesFlow.Node.Option(
                name="Brightness Max",
                option_component=NodesFlow.NumberOptionComponent(
                    min=-255, max=255, default_value=50
                ),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=None,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

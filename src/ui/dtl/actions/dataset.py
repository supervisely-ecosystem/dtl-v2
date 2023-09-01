from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class DatasetAction(Action):
    name = "dataset"
    title = "Dataset"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"
    )
    description = "This layer (dataset) places every image that it sees to dataset with a specified name. Put name of the future dataset in the field name."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "rule": None,
        "name": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            if options_json["Save original"]:
                return {
                    "rule": "save_original",
                }
            name = options_json["name"] if options_json["name"] is not None else ""
            name.strip("'\"").lstrip("'\"")
            return {
                "name": name,
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            if "rule" in settings:
                node_state["Save original"] = True
            else:
                node_state["Save original"] = False
                node_state["name"] = settings["name"]
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="rule_text",
                option_component=NodesFlow.TextOptionComponent("Rule: Save Original"),
            ),
            NodesFlow.Node.Option(
                name="Save original", option_component=NodesFlow.CheckboxOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="name_text", option_component=NodesFlow.TextOptionComponent("Name")
            ),
            NodesFlow.Node.Option(name="name", option_component=NodesFlow.InputOptionComponent()),
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

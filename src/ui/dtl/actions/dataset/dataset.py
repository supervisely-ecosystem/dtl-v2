from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow, Text, Input, Checkbox

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class DatasetAction(OtherAction):
    name = "dataset"
    title = "Dataset"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/dataset"
    description = "Places every image that it sees to dataset with a specified name."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        save_original_text = Text("Rule: Save Original", status="text")
        save_original_checkbox = Checkbox("Save Original")

        ds_name_text = Text("Name", status="text")
        ds_name_input = Input(value="", placeholder="Enter dataset name", size="small")

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            if save_original_checkbox.is_checked():
                return {
                    "rule": "save_original",
                }
            name = ds_name_input.get_value()
            name.strip("'\"").lstrip("'\"")
            return {
                "name": name,
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="rule_text",
                    option_component=NodesFlow.WidgetOptionComponent(save_original_text),
                ),
                NodesFlow.Node.Option(
                    name="Save original",
                    option_component=NodesFlow.WidgetOptionComponent(save_original_checkbox),
                ),
                NodesFlow.Node.Option(
                    name="name_text", option_component=NodesFlow.WidgetOptionComponent(ds_name_text)
                ),
                NodesFlow.Node.Option(
                    name="name", option_component=NodesFlow.WidgetOptionComponent(ds_name_input)
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

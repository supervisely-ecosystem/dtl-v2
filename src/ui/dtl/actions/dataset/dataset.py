from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer


class DatasetAction(OtherAction):
    name = "dataset"
    title = "Dataset"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"
    )
    description = "This layer (dataset) places every image that it sees to dataset with a specified name. Put name of the future dataset in the field name."

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

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

        def create_options(src: list, dst: list, settings: dict) -> dict:
            if "rule" in settings:
                save_orig_val = True
                name_val = ""
            else:
                save_orig_val = False
                name_val = settings.get("name", "")
            settings_options = [
                NodesFlow.Node.Option(
                    name="rule_text",
                    option_component=NodesFlow.TextOptionComponent("Rule: Save Original"),
                ),
                NodesFlow.Node.Option(
                    name="Save original",
                    option_component=NodesFlow.CheckboxOptionComponent(save_orig_val),
                ),
                NodesFlow.Node.Option(
                    name="name_text", option_component=NodesFlow.TextOptionComponent("Name")
                ),
                NodesFlow.Node.Option(
                    name="name", option_component=NodesFlow.InputOptionComponent(name_val)
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

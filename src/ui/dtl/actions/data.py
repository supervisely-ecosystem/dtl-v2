import copy
import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class DataAction(Action):
    name = "data"
    title = "Data"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/data-layers/data"
    description = "Data layer (data) is used to specify project and its datasets that will participate in data transformation process."

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        cls.create_info_widget()
                    )
                ),
            ),
            NodesFlow.Node.Option(
                name="source_text",
                option_component=NodesFlow.TextOptionComponent("Source"),
            ),
            NodesFlow.Node.Option(
                name="src", option_component=NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="classes_mapping_text",
                option_component=NodesFlow.TextOptionComponent("Classes Mapping"),
            ),
            NodesFlow.Node.Option(
                name="classes_mapping",
                option_component=NodesFlow.InputOptionComponent(),
            ),
        ]

    @classmethod
    def create_inputs(cls):
        return []
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        src = options["src"]
        if src is None or src == "":
            raise ValueError("Source is not specified")
        if src[0] == "[":
            src = json.loads(src)
        else:
            src = [src.strip("'\"")]
        classes_mapping = options["classes_mapping"]
        if classes_mapping[0] == "{":
            classes_mapping = json.loads(classes_mapping)
        else:
            classes_mapping = classes_mapping.strip("'\"")
        return {
            "src": src,
            "settings": {
                "classes_mapping": classes_mapping
            }
        }

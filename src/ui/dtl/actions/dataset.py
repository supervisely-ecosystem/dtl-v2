from .base import Action
from supervisely.app.widgets import NodesFlow


class DatasetAction(Action):
    name = "dataset"
    title = "Dataset"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"
    description = "This layer (dataset) places every image that it sees to dataset with a specified name. Put name of the future dataset in the field name."

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
                name="rule_text",
                option_component=NodesFlow.TextOptionComponent("Rule: Save Original"),
            ),
            NodesFlow.Node.Option(
                name="Save original", option_component=NodesFlow.CheckboxOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="name_text", option_component=NodesFlow.TextOptionComponent("Name")
            ),
            NodesFlow.Node.Option(
                name="name", option_component=NodesFlow.InputOptionComponent()
            ),
        ]

    @classmethod
    def parse_options(cls, options: dict) -> dict:
        if options["Save original"]:
            return {
                "settings": {
                    "rule": "save_original",
                }
            }
        name = options["name"].strip("'\"").lstrip("'\"")
        return {
            "settings": {
                "name": name,
            },
        }

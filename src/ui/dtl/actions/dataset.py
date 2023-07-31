from .base import Action
from supervisely.app.widgets import NodesFlow, Text


class DatasetAction(Action):
    title = "Dataset"
    name = "dataset"
    description = "This layer (dataset) places every image that it sees to dataset with a specified name."
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name = "Info",
                option_component = NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(Text(f'{cls.description}\n{cls.docs_url}'))
                )
            ),
            NodesFlow.Node.Option(
                name = "rule_text",
                option_component = NodesFlow.TextOptionComponent("Rule: Save Original")
            ),
            NodesFlow.Node.Option(
                name = "rule",
                option_component = NodesFlow.CheckboxOptionComponent()
            ),
            NodesFlow.Node.Option(
                name = "name_text",
                option_component = NodesFlow.TextOptionComponent("Name")
            ),
            NodesFlow.Node.Option(
                name = "name",
                option_component = NodesFlow.InputOptionComponent()
            )
        ]

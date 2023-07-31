from .base import Action
from supervisely.app.widgets import NodesFlow, Text


class SuperviselyAction(Action):
    title = "Supervisely"
    name = "supervisely"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/supervisely"

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name = "Info",
                option_component = NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(Text(cls.docs_url))
                )
            ),
            NodesFlow.Node.Option(
                name = "destination_text",
                option_component = NodesFlow.TextOptionComponent("Destination")
            ),
            NodesFlow.Node.Option(
                name = "dst",
                option_component = NodesFlow.InputOptionComponent()
            ),
        ]
    
    @classmethod
    def create_outputs(cls):
        return []

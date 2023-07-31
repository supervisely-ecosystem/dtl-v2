from .base import Action
from supervisely.app.widgets import NodesFlow, Text

class DataAction(Action):
    title = "Data"
    name = "data"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/data-layers/data"

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
                name = "source_text",
                option_component = NodesFlow.TextOptionComponent("Source")
            ),
            NodesFlow.Node.Option(
                name = "src",
                option_component = NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name = "classes_mapping_text",
                option_component = NodesFlow.TextOptionComponent("Classes Mapping")
            ),
            NodesFlow.Node.Option(
                name = "classes_mapping",
                option_component = NodesFlow.InputOptionComponent()
            ),
        ]
    
    @classmethod
    def create_inputs(cls):
        return []

from .base import Action
from supervisely.app.widgets import NodesFlow


class SuperviselyAction(Action):
    name = "supervisely"
    title = "Supervisely"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/save-layers/supervisely"
    )
    description = "Supervisely layer (supervisely) stores results of data transformations to a new project in your workspace. Remember that you should specify a unique name to your output project. This output project will be created automatically. Supervisely layer doesn't need any settings so just leave this field blank."

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
                name="destination_text",
                option_component=NodesFlow.TextOptionComponent("Destination"),
            ),
            NodesFlow.Node.Option(
                name="dst", option_component=NodesFlow.InputOptionComponent()
            ),
        ]

    @classmethod
    def create_outputs(cls):
        return []

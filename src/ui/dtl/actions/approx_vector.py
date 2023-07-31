from .base import Action
from supervisely.app.widgets import NodesFlow, Text


class ApproxVectorAction(Action):
    title = "Approx Vector"
    name = "approx_vector"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name = "Info",
                option_component = NodesFlow.ButtonOptionComponent(
                    sidebar_component= NodesFlow.WidgetOptionComponent(Text(cls.docs_url))
                )
            ),
            NodesFlow.Node.Option(
                name = "classes_text",
                option_component = NodesFlow.TextOptionComponent("Classes")
            ),
            NodesFlow.Node.Option(
                name = "classes",
                option_component = NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name = "epsilon_text",
                option_component = NodesFlow.TextOptionComponent("Epsilon")
            ),
            NodesFlow.Node.Option(
                name = "epsilon",
                option_component = NodesFlow.IntegerOptionComponent(min = 1, default_value = 3)
            )
        ]

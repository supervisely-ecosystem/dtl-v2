import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class IfAction(Action):
    name = "if"
    title = "If"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/if"
    description = "This layer (if) is used to split input data to several flows with a specified criterion."

    @classmethod
    def create_options(cls):
        # conditions = [
        #     ("probability", "Probability"),
        #     ("min_objects_count", "Min objects count"),
        #     ("min_height", "Min height"),
        #     ("tags", "Tags"),
        #     ("include_classes", "Include classes"),
        #     ("name_in_range", "Name in range"),
        # ]
        # items = [NodesFlow.SelectOptionComponent.Item(*condition) for condition in conditions]
        return [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        cls.create_info_widget()
                    )
                ),
            ),
            # NodesFlow.Node.Option(
            #     name="condition_name_text",
            #     option_component=NodesFlow.TextOptionComponent("Condition"),
            # ),
            # NodesFlow.Node.Option(
            #     name="condition_name",
            #     option_component=NodesFlow.SelectOptionComponent(items=items, default_value=items[0].value),
            # ),
            NodesFlow.Node.Option(
                name="condition_text",
                option_component=NodesFlow.TextOptionComponent("Condition"),
            ),
            NodesFlow.Node.Option(
                name="condition",
                option_component=NodesFlow.InputOptionComponent(),
            )
        ]
    
    @classmethod
    def create_outputs(cls):
        return [
            NodesFlow.Node.Output("destination_true", "Destination True"),
            NodesFlow.Node.Output("destination_false", "Destination False"),
        ]

    @classmethod
    def parse_options(cls, options: dict) -> dict:
        condition = json.loads(options["condition"])
        return {
            "settings": {
                "condition": condition,
            },
        }

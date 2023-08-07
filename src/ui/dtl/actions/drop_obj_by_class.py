import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class DropByClassAction(Action):
    name = "drop_obj_by_class"
    title = "Drop by Class"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/drop_obj_by_class"
    description = "This layer (drop_obj_by_class) simply removes annotations of specified classes. You can also use data layer and map unnecessary classes to __ignore__."

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
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes to remove"),
            ),
            NodesFlow.Node.Option(
                name="classes",
                option_component=NodesFlow.InputOptionComponent(),
            ),
        ]
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        classes = options["classes"]
        if classes[0] == "[":
            classes = json.loads(classes)
        else:
            classes = [classes.strip("'\"")]
        return {
            "settings": {
                "classes": classes,
            },
        }

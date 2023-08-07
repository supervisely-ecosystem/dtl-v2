import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class DuplicateObjectsAction(Action):
    name = "duplicate_objects"
    title = "Duplicate Objects"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/duplicate_objects"
    description = "This layer (duplicate_objects) clones figures of required classes."

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
                name="classes_mapping_text",
                option_component=NodesFlow.TextOptionComponent("Classes Mapping"),
            ),
            NodesFlow.Node.Option(
                name="classes_mapping",
                option_component=NodesFlow.InputOptionComponent(),
            ),
        ]
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        classes_mapping = json.loads(options["classes_mapping"])
        return {
            "settings": {
                "classes_mapping": classes_mapping
            },
        }

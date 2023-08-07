import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class RasterizeAction(Action):
    name = "rasterize"
    title = "Rasterize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/rasterize"
    description = "This layer (rasterize) converts all geometry figures to bitmaps."

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

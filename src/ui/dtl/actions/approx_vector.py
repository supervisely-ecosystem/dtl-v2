import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class ApproxVectorAction(Action):
    name = "approx_vector"
    title = "Approx Vector"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"
    description = "This layer (approx_vector) approximates vector figures: lines and polygons. The operation decreases number of vertices with Douglas-Peucker algorithm."

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
                option_component=NodesFlow.TextOptionComponent("Classes"),
            ),
            NodesFlow.Node.Option(
                name="classes", option_component=NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="epsilon_text",
                option_component=NodesFlow.TextOptionComponent("Epsilon"),
            ),
            NodesFlow.Node.Option(
                name="epsilon",
                option_component=NodesFlow.IntegerOptionComponent(
                    min=1, default_value=3
                ),
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
                "epsilon": options["epsilon"],
            }
        }

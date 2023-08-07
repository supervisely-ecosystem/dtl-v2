from .base import Action
from supervisely.app.widgets import NodesFlow


class ResizeAction(Action):
    name = "resize"
    title = "Resize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/resize"
    description = (
        "Resize layer (resize) resizes data (image + annotation) to the certain size."
    )

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
                name="width_text",
                option_component=NodesFlow.TextOptionComponent("Width"),
            ),
            NodesFlow.Node.Option(
                name="width", option_component=NodesFlow.IntegerOptionComponent(min=-1, default_value=1)
            ),
            NodesFlow.Node.Option(
                name="height_text",
                option_component=NodesFlow.TextOptionComponent("Height"),
            ),
            NodesFlow.Node.Option(
                name="height", option_component=NodesFlow.IntegerOptionComponent(min=-1, default_value=1)
            ),
            NodesFlow.Node.Option(
                name="Keep aspect ratio",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=False),
            ),
        ]
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        keep_aspect_ratio = bool(options["Keep aspect ratio"])
        width = options["width"]
        height = options["height"]
        if width*height == 0:
            raise ValueError("Width and Height must be positive")
        if not keep_aspect_ratio:
            if width == -1:
                raise ValueError("Width = -1 is not allowed when Keep aspect ratio is not enabled")
            if height == -1:
                raise ValueError("Height = -1 is not allowed when Keep aspect ratio is not enabled")
        return {
            "settings": {
                "width": width,
                "height": height,
                "aspect_ratio": {
                    "keep": keep_aspect_ratio,
                }
            },
        }

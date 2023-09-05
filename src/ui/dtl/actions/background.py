from typing import Optional
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class BackgroundAction(Action):
    name = "background"
    title = "Background"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/background"
    )
    description = "This layer (background) adds background rectangle (size equals to image size) with custom class to image annotations. This layer is used to prepare data to train Neural Network for semantic segmentation."

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "class": options_json["class"] if options_json["class"] else "",
            }

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="class_text",
                option_component=NodesFlow.TextOptionComponent("Background Class name"),
            ),
            NodesFlow.Node.Option(name="class", option_component=NodesFlow.InputOptionComponent()),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=None,
            id=layer_id,
        )

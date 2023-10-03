from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer


class BackgroundAction(AnnotationAction):
    name = "background"
    title = "Background"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/background"
    )
    description = "This layer (background) adds background rectangle (size equals to image size) with custom class to image annotations. This layer is used to prepare data to train Neural Network for semantic segmentation."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "class": options_json["class"] if options_json["class"] else "",
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            class_val = settings.get("class", "")
            settings_options = [
                NodesFlow.Node.Option(
                    name="class_text",
                    option_component=NodesFlow.TextOptionComponent("Background Class name"),
                ),
                NodesFlow.Node.Option(
                    name="class", option_component=NodesFlow.InputOptionComponent(class_val)
                ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
        )

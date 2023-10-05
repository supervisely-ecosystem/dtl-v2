from typing import Optional
import json

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class SuperviselyAction(OutputAction):
    name = "supervisely"
    title = "Supervisely"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/supervisely"
    description = "Save results of data transformations to a new project in current workspace."
    md_description = get_layer_docs()

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        def get_dst(options_json: dict) -> dict:
            dst = options_json.get("dst", None)
            if dst is None or dst == "":
                return []
            if dst[0] == "[":
                dst = json.loads(dst)
            else:
                dst = [dst.strip("'\"")]

            return dst

        def create_options(src: list, dst: list, settings: dict) -> dict:
            try:
                dst_value = dst[0]
            except IndexError:
                dst_value = ""
            dst_options = [
                NodesFlow.Node.Option(
                    name="destination_text",
                    option_component=NodesFlow.TextOptionComponent("Destination"),
                ),
                NodesFlow.Node.Option(
                    name="dst", option_component=NodesFlow.InputOptionComponent(dst_value)
                ),
            ]
            return {
                "src": [],
                "dst": dst_options,
                "settings": [],
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_dst=get_dst,
        )

    @classmethod
    def create_outputs(cls):
        return []

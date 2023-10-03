from typing import Optional
import json
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer


class SuperviselyAction(OutputAction):
    name = "supervisely"
    title = "Supervisely"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/supervisely"
    description = "Supervisely layer (supervisely) stores results of data transformations to a new project in your workspace. Remember that you should specify a unique name to your output project. This output project will be created automatically. Supervisely layer doesn't need any settings so just leave this field blank."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

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

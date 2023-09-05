from typing import Optional
import json
from supervisely.app.widgets import NodesFlow
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class SuperviselyAction(Action):
    name = "supervisely"
    title = "Supervisely"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/supervisely"
    description = "Supervisely layer (supervisely) stores results of data transformations to a new project in your workspace. Remember that you should specify a unique name to your output project. This output project will be created automatically. Supervisely layer doesn't need any settings so just leave this field blank."

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

        options = [
            NodesFlow.Node.Option(
                name="destination_text",
                option_component=NodesFlow.TextOptionComponent("Destination"),
            ),
            NodesFlow.Node.Option(name="dst", option_component=NodesFlow.InputOptionComponent()),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=None,
            get_src=None,
            meta_changed_cb=None,
            get_dst=get_dst,
            id=layer_id,
        )

    @classmethod
    def create_outputs(cls):
        return []

import json
from typing import Optional
import os
from pathlib import Path

import requests
from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class SaveAction(OutputAction):
    name = "save"
    title = "Save"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/save"
    description = (
        "Save layer (save) allows to export annotations and images. Annotations are "
        "stored in .json files. Images are stored in .png or .jpg files (due to format"
        " of source image). When exporting annotations, meta.json file containing all "
        "used classes for project is also exported. Moreover, you can get visual "
        "representations of all annotated objects on top of your images by setting "
        "visualize to true."
    )
    md_description_url = (
        "https://raw.githubusercontent.com/supervisely/docs/master/data-manipulation/dtl/save.md"
    )
    md_description = requests.get(md_description_url).text

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            visualize = bool(options_json["Visualize"])
            return {
                "visualize": visualize,
            }

        def get_dst(options_json: dict) -> dict:
            dst = options_json.get("dst", None)
            if dst is None or dst == "":
                return []
                # raise ValueError("Destination is not specified")
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
            try:
                visualize_value = settings["visualize"]
            except KeyError:
                visualize_value = False

            dst_options = [
                NodesFlow.Node.Option(
                    name="destination_text",
                    option_component=NodesFlow.TextOptionComponent("Destination"),
                ),
                NodesFlow.Node.Option(
                    name="dst", option_component=NodesFlow.InputOptionComponent(dst_value)
                ),
            ]
            settings_options = [
                NodesFlow.Node.Option(
                    name="Visualize",
                    option_component=NodesFlow.CheckboxOptionComponent(visualize_value),
                ),
            ]
            return {
                "src": [],
                "dst": dst_options,
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_dst=get_dst,
            get_settings=get_settings,
        )

    @classmethod
    def create_outputs(cls):
        return []

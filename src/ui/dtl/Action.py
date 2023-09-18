from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Optional

from supervisely.app.widgets import NodesFlow, Container, Text


class Action:
    name = None
    title = None
    docs_url = None
    description = None
    md_description = ""
    width = 340
    header_color = None
    header_text_color = None

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        raise NotImplementedError

    @classmethod
    def create_inputs(cls):
        return [NodesFlow.Node.Input("source", "Input", color="#000000")]

    @classmethod
    def create_outputs(cls):
        return [NodesFlow.Node.Output("destination", "Output", color="#000000")]

    @classmethod
    def create_info_widget(cls):
        return Container(
            widgets=[
                Text(f"<h3>{cls.title}</h3>"),
                Text(f'<a href="{cls.docs_url}" target="_blank">Docs</a>'),
                Text(f"<p>{cls.description}</p>"),
            ]
        )


class SourceAction(Action):
    header_color = "#13ce66"
    header_text_color = "#000000"


class PixelLevelAction(Action):
    header_color = "#c9a5fa"
    header_text_color = "#000000"


class SpatialLevelAction(Action):
    header_color = "#fcd068"
    header_text_color = "#000000"


class AnnotationAction(Action):
    header_color = "#90ddf5"
    header_text_color = "#000000"


class OtherAction(Action):
    header_color = "#cfcfcf"
    header_text_color = "#000000"


class OutputAction(Action):
    header_color = "#ff5e90"
    header_text_color = "#000000"

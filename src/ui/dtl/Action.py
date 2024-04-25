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
    node_color = "#cfcfcf"
    header_text_color = "#000000"
    icon = "zmdi zmdi-folder"

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

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
    node_color = "#13ce66"
    icon = "zmdi zmdi-folder"


class PixelLevelAction(Action):
    node_color = "#c9a5fa"
    icon = "zmdi zmdi-image-o"


class SpatialLevelAction(Action):
    node_color = "#fcd068"
    icon = "zmdi zmdi-collection-bookmark"


class AnnotationAction(Action):
    node_color = "#90ddf5"
    icon = "zmdi zmdi-shape"


class OtherAction(Action):
    node_color = "#cfcfcf"
    icon = "zmdi zmdi-apps"


class OutputAction(Action):
    node_color = "#ff5e90"
    icon = "zmdi zmdi-floppy"


class FilterAndConditionAction(Action):
    node_color = "#3fbfbf"
    icon = "zmdi zmdi-arrow-split"


class NeuralNetworkAction(Action):
    node_color = "#f7782f"
    icon = "zmdi zmdi-fire"


# Video specific
class VideoAction(Action):
    node_color = "#bc805b"
    icon = "zmdi zmdi-videocam"


class OtherAugmentationsAction(Action):
    node_color = "#585eff"
    icon = "zmdi zmdi-brightness-auto"


# ---

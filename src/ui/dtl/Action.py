from __future__ import annotations
from typing import Optional

from supervisely.app.widgets import NodesFlow, Container, Text
import src.globals as g


class Action:
    name = None
    title = None
    docs_url = None
    description = None
    width = 340
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {}

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        raise NotImplementedError

    @classmethod
    def create_inputs(cls):
        return [NodesFlow.Node.Input("source", "Source")]

    @classmethod
    def create_outputs(cls):
        return [NodesFlow.Node.Output("destination", "Destination")]

    @classmethod
    def create_info_widget(cls):
        return Container(
            widgets=[
                Text(f"<h3>{cls.title}</h3>", color="white"),
                Text(f'<a href="{cls.docs_url}" target="_blank" style="color: white;">Docs</a>'),
                Text(f"<p>{cls.description}</p>", color="white"),
            ]
        )

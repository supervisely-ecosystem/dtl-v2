import copy
from supervisely import Annotation
from supervisely.app.widgets import LabeledImage, NodesFlow
from supervisely.imaging.image import write as write_image
from src.ui.dtl.Action import Action


import numpy as np


import random
from typing import List, Optional


class Layer:
    def __init__(
        self,
        action: Action,
        options: List[NodesFlow.Node.Option],
        get_settings: callable,
        get_src: Optional[callable] = None,
        meta_changed_cb: Optional[callable] = None,
        get_dst: Optional[callable] = None,
        set_settings_from_json: callable = None,
        id: Optional[str] = None,
    ):
        self.action = action
        self._id = id
        if self._id is None:
            self._id = action.name + "_" + "".join(random.choice("0123456789") for _ in range(8))

        self._options = options
        self._get_settings = get_settings
        self._get_src = get_src
        self._meta_changed_cb = meta_changed_cb
        self._get_dst = get_dst
        self._set_settings_from_json = set_settings_from_json

        self._src = []
        self._settings = {}
        self._dst = []

        self.output_meta = None

        self._preview_img_url = f"static/{self._id}.jpg"
        self._ann = None

        self._add_info_option()
        self._add_preview_option()

    def _add_info_option(self):
        self._options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        self.action.create_info_widget()
                    )
                ),
            ),
            *self._options,
        ]

    def _add_preview_option(self):
        self._preview_widget = LabeledImage(enable_zoom=True)
        self._options = [
            *self._options,
            NodesFlow.Node.Option(
                name="preview_text", option_component=NodesFlow.TextOptionComponent("Preview")
            ),
            NodesFlow.Node.Option(
                name="preview",
                option_component=NodesFlow.WidgetOptionComponent(widget=self._preview_widget),
            ),
        ]

    def to_json(self) -> dict:
        return {
            "action": self.action.name,
            "src": self._src,  # always list
            "dst": self._dst[0] if len(self._dst) == 1 else self._dst,  # can be str if only one dst
            "settings": self._settings,
        }

    def get_destination_name(self, dst_index: int):
        outputs = self.action.create_outputs()
        return outputs[dst_index].name

    def set_settings_from_json(self, json_data: dict, node_state: dict):
        node_state = copy.deepcopy(node_state)
        settings = json_data["settings"]
        for settings_key, value in settings.items():
            node_state_key = self.action._settings_mapping.get(settings_key, settings_key)
            if node_state_key is not None:
                node_state[node_state_key] = value
        if self._set_settings_from_json is not None:
            node_state = self._set_settings_from_json(json_data, node_state)
        return node_state

    def create_node(self) -> NodesFlow.Node:
        self._inputs = self.action.create_inputs()
        self._outputs = self.action.create_outputs()
        return NodesFlow.Node(
            id=self._id,
            name=self.action.title,
            width=self.action.width,
            options=self._options,
            inputs=self._inputs,
            outputs=self._outputs,
        )

    def update_src(self, node_options: dict):
        if self._get_src is not None:
            self._src = self._get_src(options_json=node_options)
        else:
            self._src = []

    def update_dst(self, node_options: dict):
        if self._get_dst is not None:
            self._dst = self._get_dst(options_json=node_options)
        else:
            self._dst = self._create_destinations()

    def update_settings(self, node_options: dict):
        if self._get_settings is not None:
            self._settings = self._get_settings(options_json=node_options)
        else:
            self._settings = {}

    def parse_options(self, node_options: dict):
        self.update_src(node_options)
        self.update_dst(node_options)
        self.update_settings(node_options)

    def add_source(self, from_node_id, from_node_interface):
        src_name = self._connection_name(from_node_id, from_node_interface)
        self._src.append(src_name)

    def _connection_name(self, name: str, interface: str):
        interface_str = "_".join(
            [
                *[
                    part
                    for part in interface.split("_")
                    if part not in ["", "source", "destination"]
                ],
            ]
        )
        return "$" + name + (f"__{interface_str}" if interface_str else "")

    def _create_destinations(self):
        return [self._connection_name(self._id, output.name) for output in self._outputs]

    def clear_sources(self):
        self._src = []

    def clear_destinations(self):
        self._dst = []

    def clear_settings(self):
        self._settings = {}

    def clear(self):
        self.clear_sources()
        self.clear_destinations()
        self.clear_settings()

    def get_src(self):
        return self._src

    def get_dst(self):
        return self._dst

    def set_preview(self, img: np.ndarray, ann: Annotation):
        write_image(self._preview_img_url, img)
        self._ann = ann
        self._preview_widget.set(title=None, image_url=self._preview_img_url, ann=self._ann)

    def get_ann(self):
        return self._ann

    def meta_changed_cb(self, project_meta):
        if self._meta_changed_cb is not None:
            self._meta_changed_cb(project_meta)

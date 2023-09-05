import json
from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class SaveAction(Action):
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
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "visualize": "Visualize",
    }

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

        options = [
            NodesFlow.Node.Option(
                name="destination_text",
                option_component=NodesFlow.TextOptionComponent("Destination"),
            ),
            NodesFlow.Node.Option(name="dst", option_component=NodesFlow.InputOptionComponent()),
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="Visualize",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=get_dst,
            id=layer_id,
        )

    @classmethod
    def create_outputs(cls):
        return []

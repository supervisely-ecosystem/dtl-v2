from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import PixelLevelAction
from src.ui.dtl.Layer import Layer


class ContrastBrightnessAction(PixelLevelAction):
    name = "contrast_brightness"
    title = "Contrast / Brightness"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/contrast_brightness"
    description = (
        "This layer (contrast_brightness) randomly changes contrast and brightness of images. "
    )

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            settings = {}
            if options_json["Contrast"]:
                settings["contrast"] = {
                    "min": options_json["Contrast Min"],
                    "max": options_json["Contrast Max"],
                    "center_grey": options_json["Center grey"]
                    if options_json["Center grey"]
                    else False,
                }
            else:
                settings["contrast"] = {
                    "min": 1,
                    "max": 1,
                    "center_grey": False,
                }
            if options_json["Brightness"]:
                settings["brightness"] = {
                    "min": options_json["Brightness Min"],
                    "max": options_json["Brightness Max"],
                }
            else:
                settings["brightness"] = {
                    "min": 0,
                    "max": 0,
                }
            return settings

        def create_options(src: list, dst: list, settings: dict) -> dict:
            contrast_val = False
            contrast_min_val = 1
            contrast_max_val = 2
            center_grey_val = False
            if "contrast" in settings:
                contrast_val = True
                contrast_min_val = settings["contrast"].get("min", 1)
                contrast_max_val = settings["contrast"].get("max", 2)
                center_grey_val = settings["contrast"].get("center_grey", False)
            brightness_val = False
            brightness_min_val = -50
            brightness_max_val = 50
            if "brightness" in settings:
                brightness_val = True
                brightness_min_val = settings["brightness"].get("min", -50)
                brightness_max_val = settings["brightness"].get("max", 50)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Contrast",
                    option_component=NodesFlow.CheckboxOptionComponent(default_value=contrast_val),
                ),
                NodesFlow.Node.Option(
                    name="Contrast Min",
                    option_component=NodesFlow.SliderOptionComponent(
                        min=0, max=10, default_value=contrast_min_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Contrast Max",
                    option_component=NodesFlow.SliderOptionComponent(
                        min=0, max=10, default_value=contrast_max_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Center grey",
                    option_component=NodesFlow.CheckboxOptionComponent(
                        default_value=center_grey_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="center_grey_text",
                    option_component=NodesFlow.TextOptionComponent(
                        '*To center colors of images (subtract 128) first, set "Center grey" to true'
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Brightness",
                    option_component=NodesFlow.CheckboxOptionComponent(
                        default_value=brightness_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Brightness Min",
                    option_component=NodesFlow.SliderOptionComponent(
                        min=-255, max=255, default_value=brightness_min_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Brightness Max",
                    option_component=NodesFlow.SliderOptionComponent(
                        min=-255, max=255, default_value=brightness_max_val
                    ),
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

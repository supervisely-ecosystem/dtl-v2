from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow, Slider, Text

from src.ui.dtl import PixelLevelAction
from src.ui.dtl.Layer import Layer


class ContrastBrightnessAction(PixelLevelAction):
    name = "contrast_brightness"
    title = "Contrast / Brightness"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/contrast_brightness"
    description = (
        "This layer (contrast_brightness) randomly changes contrast and brightness of images. "
    )

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        contrast_slider = Slider(
            min=0,
            max=10,
            step=0.1,
            value=[1, 1],
            range=True,
        )
        brightness_slider = Slider(min=-255, max=255, step=1, value=[0, 0], range=True)
        contrast_preview_widget = Text("min: 1 - max: 1")
        brightness_preview_widget = Text("min: 0 - max: 0")

        @contrast_slider.value_changed
        def contrast_slider_value_changed(value):
            contrast_preview_widget.text = f"min: {value[0]} - max: {value[1]}"

        @brightness_slider.value_changed
        def brightness_slider_value_changed(value):
            brightness_preview_widget.text = f"min: {value[0]} - max: {value[1]}"

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            settings = {}

            if options_json["Contrast"]:
                contrast_min, contrast_max = contrast_slider.get_value()
                settings["contrast"] = {
                    "min": contrast_min,
                    "max": contrast_max,
                    "center_grey": options_json[
                        "Center grey. Center colors of images (subtract 128) first"
                    ]
                    if options_json["Center grey. Center colors of images (subtract 128) first"]
                    else False,
                }
            else:
                settings["contrast"] = {
                    "min": 1,
                    "max": 1,
                    "center_grey": False,
                }
            if options_json["Brightness"]:
                brightness_min, brightness_max = brightness_slider.get_value()
                settings["brightness"] = {
                    "min": brightness_min,
                    "max": brightness_max,
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
            contrast_max_val = 1
            center_grey_val = False
            if "contrast" in settings:
                contrast_val = True
                contrast_min_val = settings["contrast"].get("min", 1)
                contrast_max_val = settings["contrast"].get("max", 1)
                center_grey_val = settings["contrast"].get("center_grey", False)
            contrast_slider.set_value([contrast_min_val, contrast_max_val])
            brightness_val = False
            brightness_min_val = 0
            brightness_max_val = 0
            if "brightness" in settings:
                brightness_val = True
                brightness_min_val = settings["brightness"].get("min", 0)
                brightness_max_val = settings["brightness"].get("max", 0)
            brightness_slider.set_value([brightness_min_val, brightness_max_val])
            settings_options = [
                NodesFlow.Node.Option(
                    name="Contrast",
                    option_component=NodesFlow.CheckboxOptionComponent(default_value=contrast_val),
                ),
                NodesFlow.Node.Option(
                    name="Center grey. Center colors of images (subtract 128) first",
                    option_component=NodesFlow.CheckboxOptionComponent(
                        default_value=center_grey_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="contrast_preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=contrast_preview_widget,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="contrast_slider",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=contrast_slider,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Brightness",
                    option_component=NodesFlow.CheckboxOptionComponent(
                        default_value=brightness_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="brightness_preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=brightness_preview_widget,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="brightness_slider",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=brightness_slider,
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

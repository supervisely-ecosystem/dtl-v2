from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import (
    NodesFlow,
    Select,
    InputNumber,
    Switch,
    Container,
    Field,
    Flexbox,
    OneOf,
    Checkbox,
    Button,
    Text,
)

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_set_settings_button_style, get_set_settings_container


class CropAction(SpatialLevelAction):
    name = "crop"
    title = "Crop"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/crop"
    description = "This layer (crop) is used to crop part of image with its annotations. This layer has several modes: it may crop fixed given part of image or random one."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        crop_fixed_top_px = InputNumber(min=0)
        crop_fixed_top_percent = InputNumber(min=0, max=100)
        crop_fixed_top_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=crop_fixed_top_px,
            off_content=crop_fixed_top_percent,
        )
        crop_fixed_left_px = InputNumber(min=0)
        crop_fixed_left_percent = InputNumber(min=0, max=100)
        crop_fixed_left_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=crop_fixed_left_px,
            off_content=crop_fixed_left_percent,
        )
        crop_fixed_right_px = InputNumber(min=0)
        crop_fixed_right_percent = InputNumber(min=0, max=100)
        crop_fixed_right_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=crop_fixed_right_px,
            off_content=crop_fixed_right_percent,
        )
        crop_fixed_bot_px = InputNumber(min=0)
        crop_fixed_bot_percent = InputNumber(min=0, max=100)
        crop_fixed_bot_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=crop_fixed_bot_px,
            off_content=crop_fixed_bot_percent,
        )
        crop_fixed_container = Container(
            widgets=[
                Field(
                    title="top",
                    content=Flexbox(widgets=[OneOf(crop_fixed_top_switch), crop_fixed_top_switch]),
                ),
                Field(
                    title="left",
                    content=Flexbox(
                        widgets=[OneOf(crop_fixed_left_switch), crop_fixed_left_switch]
                    ),
                ),
                Field(
                    title="right",
                    content=Flexbox(
                        widgets=[OneOf(crop_fixed_right_switch), crop_fixed_right_switch]
                    ),
                ),
                Field(
                    title="bottom",
                    content=Flexbox(widgets=[OneOf(crop_fixed_bot_switch), crop_fixed_bot_switch]),
                ),
            ]
        )
        crop_random_height_min = InputNumber(min=0, max=100)
        crop_random_height_max = InputNumber(min=0, max=100)
        crop_random_height = Container(
            widgets=[
                Field(
                    title="min %",
                    description="minimum height of resulting crop (in percent wrt to image height)",
                    content=crop_random_height_min,
                ),
                Field(
                    title="max %",
                    description="maximum height of resulting crop (in percent wrt to image height)",
                    content=crop_random_height_max,
                ),
            ]
        )
        crop_random_width_min = InputNumber(min=0, max=100)
        crop_random_width_max = InputNumber(min=0, max=100)
        crop_random_width = Container(
            widgets=[
                Field(
                    title="min %",
                    description="minimum width of resulting crop (in percent wrt to image width)",
                    content=crop_random_width_min,
                ),
                Field(
                    title="max %",
                    description="maximum width of resulting crop (in percent wrt to image width)",
                    content=crop_random_width_max,
                ),
            ]
        )
        crop_random_keep_aspect_ratio = Checkbox(content="Keep aspect ratio")
        crop_random_container = Container(
            widgets=[
                Field(title="Height", content=crop_random_height),
                Field(title="Width", content=crop_random_width),
                Field(
                    title="Keep aspect ratio",
                    description="should resulting random crop have the same aspect ratio as a source image",
                    content=crop_random_keep_aspect_ratio,
                ),
            ]
        )
        mode_select = Select(
            items=[
                Select.Item("sides", "Sides", crop_fixed_container),
                Select.Item("random_part", "Random part", crop_random_container),
            ]
        )

        mode_preview = Text("")
        params_preview = Text("")
        settings_preview = Container(widgets=[mode_preview, params_preview], gap=1)

        save_settings_btn = Button("Save", icon="zmdi zmdi-floppy")
        settings_container = Container(widgets=[mode_select, OneOf(mode_select), save_settings_btn])
        settings_edit_text = Text("Settings")
        settings_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        settings_edit_container = get_set_settings_container(settings_edit_text, settings_edit_btn)

        saved_settings = {}

        def _set_sides(settings: dict):
            mode_select.set_value("sides")
            top_value = settings["sides"]["top"]
            if top_value.endswith("px"):
                crop_fixed_top_px.value = int(top_value[:-2])
                crop_fixed_top_switch.on()
            else:
                crop_fixed_top_percent.value = int(top_value[:-1])
                crop_fixed_top_switch.off()
            left_value = settings["sides"]["left"]
            if left_value.endswith("px"):
                crop_fixed_left_px.value = int(left_value[:-2])
                crop_fixed_left_switch.on()
            else:
                crop_fixed_left_percent.value = int(left_value[:-1])
                crop_fixed_left_switch.off()
            right_value = settings["sides"]["right"]
            if right_value.endswith("px"):
                crop_fixed_right_px.value = int(right_value[:-2])
                crop_fixed_right_switch.on()
            else:
                crop_fixed_right_percent.value = int(right_value[:-1])
                crop_fixed_right_switch.off()
            bot_value = settings["sides"]["bottom"]
            if bot_value.endswith("px"):
                crop_fixed_bot_px.value = int(bot_value[:-2])
                crop_fixed_bot_switch.on()
            else:
                crop_fixed_bot_percent.value = int(bot_value[:-1])
                crop_fixed_bot_switch.off()

        def _get_sides():
            return {
                "top": str(crop_fixed_top_px.get_value()) + "px"
                if crop_fixed_top_switch.is_switched()
                else str(crop_fixed_top_percent.get_value()) + "%",
                "left": str(crop_fixed_left_px.get_value()) + "px"
                if crop_fixed_left_switch.is_switched()
                else str(crop_fixed_left_percent.get_value()) + "%",
                "right": str(crop_fixed_right_px.get_value()) + "px"
                if crop_fixed_right_switch.is_switched()
                else str(crop_fixed_right_percent.get_value()) + "%",
                "bottom": str(crop_fixed_bot_px.get_value()) + "px"
                if crop_fixed_bot_switch.is_switched()
                else str(crop_fixed_bot_percent.get_value()) + "%",
            }

        def _set_random(settings: dict):
            crop_random_height_min.value = settings["random_part"]["height"]["min_percent"]
            crop_random_height_max.value = settings["random_part"]["height"]["max_percent"]
            crop_random_width_min.value = settings["random_part"]["width"]["min_percent"]
            crop_random_width_max.value = settings["random_part"]["width"]["max_percent"]
            if settings["random_part"]["keep_aspect_ratio"]:
                crop_random_keep_aspect_ratio.check()
            else:
                crop_random_keep_aspect_ratio.uncheck()

        def _get_random():
            return {
                "height": {
                    "min_percent": crop_random_height_min.get_value(),
                    "max_percent": crop_random_height_max.get_value(),
                },
                "width": {
                    "min_percent": crop_random_width_min.get_value(),
                    "max_percent": crop_random_width_max.get_value(),
                },
                "keep_aspect_ratio": crop_random_keep_aspect_ratio.is_checked(),
            }

        def _update_preview():
            mode = "sides" if "sides" in saved_settings else "random_part"
            if mode == "":
                mode_preview.text = ""
                params_preview.text = ""
            elif mode == "sides":
                sides = _get_sides()
                mode_preview.text = "Mode: Sides"
                params_preview.text = f"Top: {sides['top']}; Left: {sides['left']}; Right: {sides['right']}; Bottom: {sides['bottom']}"
            elif mode == "random_part":
                random_part = _get_random()
                mode_preview.text = "Mode: Random part"
                params_preview.text = f"Height: {random_part['height']['min_percent']} - {random_part['height']['max_percent']}; Width: {random_part['width']['min_percent']} - {random_part['width']['max_percent']}; Keep aspect ratio: {random_part['keep_aspect_ratio']}"

        def _save_settings():
            nonlocal saved_settings
            settings = {}
            mode = mode_select.get_value()
            if mode == "sides":
                settings["sides"] = _get_sides()
            else:
                settings["random_part"] = _get_random()
            saved_settings = settings
            _update_preview()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings):
            if "sides" in settings:
                _set_sides(settings)
            elif "random_part" in settings:
                _set_random(settings)
            _save_settings()

        save_settings_btn.click(_save_settings)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Settings",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=settings_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(settings_container),
                    ),
                ),
                NodesFlow.Node.Option(
                    name="settings_preview",
                    option_component=NodesFlow.WidgetOptionComponent(settings_preview),
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

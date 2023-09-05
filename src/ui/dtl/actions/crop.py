from typing import Optional
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
)
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class CropAction(Action):
    name = "crop"
    title = "Crop"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/crop"
    description = "This layer (crop) is used to crop part of image with its annotations. This layer has several modes: it may crop fixed given part of image or random one."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {"sides": None, "random_part": None}

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

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            settings = {}
            if mode_select.get_value() == "sides":
                settings["sides"] = _get_sides()
            else:
                settings["random_part"] = _get_random()
            return settings

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            if "sides" in settings:
                _set_sides(settings)
            else:
                _set_random(settings)
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Crop settings"),
            ),
            NodesFlow.Node.Option(
                name="Set Settings",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        Container(widgets=[mode_select, OneOf(mode_select)])
                    )
                ),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=None,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

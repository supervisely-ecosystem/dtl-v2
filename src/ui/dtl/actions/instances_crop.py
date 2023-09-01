from typing import Optional
from supervisely import ProjectMeta
from supervisely.app.widgets import (
    NodesFlow,
    InputNumber,
    Switch,
    Container,
    Field,
    Flexbox,
    OneOf,
)
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class InstancesCropAction(Action):
    name = "instances_crop"
    title = "Instances Crop"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/instances_crop"
    )
    description = "This layer (instances_crop) crops objects of specified classes from image with configurable padding. So from one image there can be produced multiple images, each with one target object: other objects are removed from crop."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes": None,
        "pad": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes = ClassesList(multiple=True)

        padding_top_px = InputNumber(min=0)
        padding_top_percent = InputNumber(min=0, max=100)
        padding_top_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=padding_top_px,
            off_content=padding_top_percent,
        )
        padding_left_px = InputNumber(min=0)
        padding_left_percent = InputNumber(min=0, max=100)
        padding_left_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=padding_left_px,
            off_content=padding_left_percent,
        )
        padding_right_px = InputNumber(min=0)
        padding_right_percent = InputNumber(min=0, max=100)
        padding_right_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=padding_right_px,
            off_content=padding_right_percent,
        )
        padding_bot_px = InputNumber(min=0)
        padding_bot_percent = InputNumber(min=0, max=100)
        padding_bot_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=padding_bot_px,
            off_content=padding_bot_percent,
        )
        padding_container = Container(
            widgets=[
                Field(
                    title="top",
                    content=Flexbox(widgets=[OneOf(padding_top_switch), padding_top_switch]),
                ),
                Field(
                    title="left",
                    content=Flexbox(widgets=[OneOf(padding_left_switch), padding_left_switch]),
                ),
                Field(
                    title="right",
                    content=Flexbox(widgets=[OneOf(padding_right_switch), padding_right_switch]),
                ),
                Field(
                    title="bottom",
                    content=Flexbox(widgets=[OneOf(padding_bot_switch), padding_bot_switch]),
                ),
            ]
        )

        def _get_padding():
            return {
                "sides": {
                    "top": f"{padding_top_px.value}px"
                    if padding_top_switch.is_switched()
                    else f"{padding_top_percent.value}%",
                    "left": f"{padding_left_px.value}px"
                    if padding_left_switch.is_switched()
                    else f"{padding_left_percent.value}%",
                    "right": f"{padding_right_px.value}px"
                    if padding_right_switch.is_switched()
                    else f"{padding_right_percent.value}%",
                    "bottom": f"{padding_bot_px.value}px"
                    if padding_bot_switch.is_switched()
                    else f"{padding_bot_percent.value}%",
                }
            }

        def _set_padding(settings: dict):
            padding = settings["pad"]["sides"]
            top_value = padding["top"]
            if top_value.endswith("px"):
                padding_top_px.value = int(top_value[:-2])
                padding_top_switch.on()
            else:
                padding_top_percent.value = int(top_value[:-1])
                padding_top_switch.off()
            left_value = padding["left"]
            if left_value.endswith("px"):
                padding_left_px.value = int(left_value[:-2])
                padding_left_switch.on()
            else:
                padding_left_percent.value = int(left_value[:-1])
                padding_left_switch.off()
            right_value = padding["right"]
            if right_value.endswith("px"):
                padding_right_px.value = int(right_value[:-2])
                padding_right_switch.on()
            else:
                padding_right_percent.value = int(right_value[:-1])
                padding_right_switch.off()
            bot_value = padding["bottom"]
            if bot_value.endswith("px"):
                padding_bot_px.value = int(bot_value[:-2])
                padding_bot_switch.on()
            else:
                padding_bot_percent.value = int(bot_value[:-1])
                padding_bot_switch.off()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": [cls.name for cls in classes.get_selected_classes()],
                "pad": _get_padding(),
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            classes.loading = True
            padding_container.loading = True
            classes.select(settings["classes"])
            _set_padding(settings)
            classes.loading = False
            padding_container.loading = False
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            classes.loading = True
            classes.set(project_meta.obj_classes)
            classes.loading = False

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes"),
            ),
            NodesFlow.Node.Option(
                name="Select Classes",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes)
                ),
            ),
            NodesFlow.Node.Option(
                name="padding_text",
                option_component=NodesFlow.TextOptionComponent("Padding"),
            ),
            NodesFlow.Node.Option(
                name="Set Padding",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(padding_container)
                ),
            ),
        ]
        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=meta_changed_cb,
            get_dst=None,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

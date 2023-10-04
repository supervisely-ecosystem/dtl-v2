from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import (
    NodesFlow,
    Container,
    Select,
    InputNumber,
    OneOf,
    Field,
    Flexbox,
    Text,
    Button,
)

from src.ui.dtl import PixelLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_set_settings_button_style, get_set_settings_container


class BlurAction(PixelLevelAction):
    name = "blur"
    title = "Blur"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/blur"
    description = 'Blur layer ("action": "blur") applies blur filter to the image. To use median blur (cv2.medianBlur) set name to median and kernel to odd number. To use gaussian blur (cv2.GaussianBlur) set name to gaussian and sigma to object with two numbers: min and max.'

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _cur_kernel = 5
        kernel_input = InputNumber(value=_cur_kernel, min=3, step=2)
        sigma_min_input = InputNumber(value=3, min=0.01, step=0.01)
        sigma_max_input = InputNumber(value=50, min=0.01, step=0.01)
        select_name = Select(
            items=[
                Select.Item(
                    "median",
                    "Median",
                    Field(
                        title="Kernel", description="Set kernel to odd number", content=kernel_input
                    ),
                ),
                Select.Item(
                    "gaussian",
                    "Gaussian",
                    Field(
                        title="Sigma",
                        content=Container(
                            widgets=[
                                Flexbox(widgets=[Text("Min"), sigma_min_input]),
                                Flexbox(widgets=[Text("Max"), sigma_max_input]),
                            ]
                        ),
                    ),
                ),
            ]
        )
        save_settings_button = Button("Save", icon="zmdi zmdi-floppy")
        settings_widget = Container(
            widgets=[
                Field(title="Blur type", content=select_name),
                OneOf(select_name),
                save_settings_button,
            ]
        )
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

        type_preview = Text("")
        params_preview = Text("")
        settings_preview = Container(widgets=[type_preview, params_preview], gap=1)

        saved_settings = {}

        def _update_preview():
            blur_type = saved_settings.get("name", "")
            type_preview.text = f"Blur type: {blur_type}"
            if blur_type == "":
                params_preview.text = ""
            elif blur_type == "median":
                params_preview.text = f"kernel = {saved_settings.get('kernel')}"
            elif blur_type == "gaussian":
                params_preview.text = (
                    f'sigma = {saved_settings["sigma"]["min"]} - {saved_settings["sigma"]["max"]}'
                )

        def _save_settings():
            nonlocal saved_settings
            settings = {
                "name": select_name.get_value(),
            }
            if settings["name"] == "median":
                settings["kernel"] = kernel_input.get_value()
            else:
                settings["sigma"] = {
                    "min": sigma_min_input.get_value(),
                    "max": sigma_max_input.get_value(),
                }
            saved_settings = settings
            _update_preview()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings: dict):
            settings_widget.loading = True
            name = settings.get("name", "median")
            select_name.set_value(name)
            if name == "median":
                kernel_input.value = settings.get("kernel", 5)
            else:
                sigma_min_v = settings.get("sigma", {}).get("min", 3)
                sigma_max_v = settings.get("sigma", {}).get("max", 50)
                sigma_min_input.value = sigma_min_v
                sigma_max_input.value = sigma_max_v
            _save_settings()
            settings_widget.loading = False

        save_settings_button.click(_save_settings)

        @kernel_input.value_changed
        def kernel_input_cb(value):
            nonlocal _cur_kernel
            if value % 2 == 0:
                kernel_input.value = _cur_kernel
            else:
                _cur_kernel = value

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Settings",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=settings_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(settings_widget),
                        sidebar_width=300,
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

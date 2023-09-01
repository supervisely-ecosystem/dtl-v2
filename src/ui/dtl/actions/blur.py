from typing import Optional
from supervisely.app.widgets import NodesFlow, Container, Select, InputNumber, OneOf
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer


class BlurAction(Action):
    name = "blur"
    title = "Blur"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/blur"
    description = 'Blur layer ("action": "blur") applies blur filter to the image. To use median blur (cv2.medianBlur) set name to median and kernel to odd number. To use gaussian blur (cv2.GaussianBlur) set name to gaussian and sigma to object with two numbers: min and max.'
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "name": None,
        "kernel": None,
        "sigma": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        kernel_input = InputNumber(value=5, min=3, step=2)
        sigma_min_input = InputNumber(value=3, min=0.01, step=0.01)
        sigma_max_input = InputNumber(value=50, min=0.01, step=0.01)
        select_name = Select(
            items=[
                Select.Item("median", "Median", kernel_input),
                Select.Item(
                    "gaussian", "Gaussian", Container(widgets=[sigma_min_input, sigma_max_input])
                ),
            ]
        )
        settings_widget = Container(widgets=[select_name, OneOf(select_name)])

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
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
            return settings

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            settings_widget.loading = True
            select_name.set_value(settings["name"])
            if settings["name"] == "median":
                kernel_input.value = settings["kernel"]
            else:
                sigma_min_input.value = settings["sigma"]["min"]
                sigma_max_input.value = settings["sigma"]["max"]
            settings_widget.loading = False
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="Set Settings",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(settings_widget)
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

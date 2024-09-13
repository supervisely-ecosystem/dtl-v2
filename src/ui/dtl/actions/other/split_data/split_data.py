from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

from supervisely.app.widgets import NodesFlow
from src.ui.dtl.actions.other.split_data.layout.split_data_sidebar import create_sidebar_widgets
from src.ui.dtl.actions.other.split_data.layout.split_data_layout import create_layout_widgets


class SplitDataAction(OtherAction):
    name = "split_data"
    title = "Split Data"
    docs_url = ""
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        saved_settings = {"split_method": "", "split_ratio": 0, "split_num": 0}
        (
            sidebar_selector,
            sidebar_selector_field,
            sidebar_percent_slider,
            sidebar_percent_field,
            sidebar_number_input,
            sidebar_number_field,
            sidebar_save_button,
        ) = create_sidebar_widgets()

        layout_text, layout_edit_button, layout_container, layout_current_method = (
            create_layout_widgets()
        )

        layout_current_method.set(f"Current method: {sidebar_selector.get_label()}", "text")

        @sidebar_selector.value_changed
        def selector_cb(value):
            if value == "percent":
                sidebar_percent_field.show()
                sidebar_number_field.hide()
            elif value == "number":
                sidebar_percent_field.hide()
                sidebar_number_field.show()
            else:
                sidebar_percent_field.hide()
                sidebar_number_field.hide()

        @sidebar_save_button.click
        def save_cb():
            layout_current_method.set(f"Current method: {sidebar_selector.get_label()}", "text")
            nonlocal saved_settings
            method = sidebar_selector.get_value()
            ratio = sidebar_percent_slider.get_value()
            num = sidebar_number_input.get_value()
            saved_settings = {"split_method": method, "split_ratio": ratio, "split_num": num}

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="Layout",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(sidebar_selector_field),
                        sidebar_width=680,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Method preview",
                    option_component=NodesFlow.WidgetOptionComponent(widget=layout_current_method),
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
            need_preview=False,
        )

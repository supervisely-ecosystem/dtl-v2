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
    description = "Splits the data into datasets based on condition"
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        (
            sidebar_selector,
            sidebar_selector_field,
            sidebar_percent_slider,
            sidebar_percent_field,
            sidebar_number_input,
            sidebar_number_field,
            sidebar_save_button,
        ) = create_sidebar_widgets()

        (
            layout_text,
            layout_edit_button,
            layout_container,
            layout_current_method,
            layout_current_value,
            layout_texts_container,
        ) = create_layout_widgets()

        saved_settings = {}

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
            saved_settings = {
                "split_method": sidebar_selector.get_value(),
                "split_ratio": sidebar_percent_slider.get_value(),
                "split_num": sidebar_number_input.get_value(),
            }
            _set_settings_from_json(saved_settings)

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def _set_settings_from_json(settings: dict):
            nonlocal saved_settings
            method = settings.get("split_method", "percent")
            ratio = settings.get("split_ratio", 50)
            num = settings.get("split_num", 50)

            saved_settings = {
                "split_method": method,
                "split_ratio": ratio,
                "split_num": num,
            }

            layout_current_method.set(f"Current method: {method}", "text")
            if method == "percent":
                layout_current_value.show()
                layout_current_value.set(
                    f"Split value: {ratio}%",
                    "text",
                )
            elif method == "number":
                layout_current_value.show()
                layout_current_value.set(
                    f"Split value: {num} items per dataset",
                    "text",
                )
            else:
                layout_current_value.hide()

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
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
                    name="Texts",
                    option_component=NodesFlow.WidgetOptionComponent(widget=layout_texts_container),
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

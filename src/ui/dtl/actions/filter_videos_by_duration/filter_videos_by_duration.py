import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta
from supervisely.app.widgets import NodesFlow, Container, Text, InputNumber, Select, Field

from src.ui.dtl.Action import FilterAndConditionAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_classes_list_value,
    get_layer_docs,
    get_text_font_size,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    classes_list_settings_changed_meta,
)
import src.globals as g


class FilterVideoByDuration(FilterAndConditionAction):
    name = "filter_video_by_duration"
    title = "Filter Video by Duration"
    docs_url = ""
    description = "Filter Videos based on their duration."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()

        settings_edit_text = Text("Duration unit", status="text", font_size=get_text_font_size())
        measure_unit_selector_items = [
            Select.Item(value="frames", label="Frames"),
            Select.Item(value="seconds", label="Seconds"),
        ]
        duration_unit_selector = Select(measure_unit_selector_items, size="small")

        filter_dur_text = Text("Max duration", status="text", font_size=get_text_font_size())
        filter_dur_input = InputNumber(value=30, step=1, controls=True, size="small")
        duration_settings = Field(
            title="Select max duration",
            description="Videos with duration less than selected will be filtered out to the output branch 'True'"
            content=filter_dur_input
            [max_dur_text, min_dur_input], columns=2
        )

        settings_container = Container(
            widgets=[settings_edit_text, duration_unit_selector, duration_settings],
        )
        saved_settings = {}

        def _save_settings():
            nonlocal saved_settings
            settings = {
                "duration_unit": duration_unit_selector.get_value(),
                "min_duration": min_dur_input.get_value(),
                "max_duration": max_dur_input.get_value(),
            }

            saved_settings = settings

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings: dict):
            duration_unit = settings.get("duration_unit", "frames")
            duration_unit_selector.set_value(duration_unit)
            min_dur = settings.get("min_duration", 0)
            min_dur_input.value = min_dur
            max_dur = settings.get("max_duration", 30)
            max_dur_input.value = max_dur
            _save_settings()

        @min_dur_input.value_changed
        def min_dur_input_cb(value):
            if value > max_dur_input.value:
                max_dur_input.value = value
            _save_settings()

        @max_dur_input.value_changed
        def max_dur_input_cb(value):
            if value < min_dur_input.value:
                min_dur_input.value = value
            _save_settings()

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Settings",
                    option_component=NodesFlow.WidgetOptionComponent(settings_container),
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

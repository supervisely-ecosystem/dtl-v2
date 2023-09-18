from typing import Optional
import os
from pathlib import Path

from supervisely import ProjectMeta
from supervisely.app.widgets import (
    NodesFlow,
    Select,
    Container,
    InputNumber,
    Field,
    OneOf,
    Button,
    Text,
)

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList, ClassesListPreview


class ObjectsFilterAction(AnnotationAction):
    name = "objects_filter"
    title = "Objects Filter"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/objects_filter"
    )
    description = "This layer (objects_filter) deletes annotations less (or greater) than specified size or percentage of image area."

    try:
        with open(Path(os.path.realpath(__file__)).parent.joinpath("readme.md")) as f:
            md_description = f.read()
    except:
        md_description = ""

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes = ClassesList(multiple=True)
        classes_field = Field(title="Select Classes", content=classes)
        percent_input = InputNumber(min=0, max=100, value=5)
        percent_input_field = Field(
            title="Input %",
            description="Filter annotations that have area (in percentage of image area) less/more than specified value",
            content=percent_input,
        )
        width_input = InputNumber(min=0, value=100)
        height_input = InputNumber(min=0, value=100)
        size_input = Container(
            widgets=[
                Field(title="Width", content=width_input),
                Field(title="Height", content=height_input),
            ]
        )
        size_input_field = Field(
            title="Input size",
            description="Filter annotations that have some side (determined by the annotation bounding box) less/more than specified value of width or height correspondingly.",
            content=size_input,
        )
        comparator_select = Select(
            items=[Select.Item("less", "Less"), Select.Item("greater", "Greater")]
        )
        comparator_select_field = Field(title="Comparator", content=comparator_select)
        action_select = Select(items=[Select.Item("delete", "Delete")])
        action_select_field = Field(title="Action", content=action_select)
        action_select.disable()
        filter_items = [
            Select.Item("names", "Names", classes),
            Select.Item(
                "area_percent",
                "Area percent",
                Container(
                    widgets=[
                        classes_field,
                        percent_input_field,
                        comparator_select_field,
                        action_select_field,
                    ]
                ),
            ),
            Select.Item(
                "bbox_size",
                "Bounding box size",
                Container(
                    widgets=[
                        classes_field,
                        size_input_field,
                        comparator_select_field,
                        action_select_field,
                    ]
                ),
            ),
        ]
        filter_by_select = Select(filter_items)
        filter_by_inputs = OneOf(filter_by_select)

        filter_by_preview_text = Text("")
        filter_preview_classes_text = Text("Classes:")
        classes_preview = ClassesListPreview()
        area_size_preview = Text("")
        comparator_preview = Text("")
        action_preview = Text("")

        filter_by_name_preview_container = Container(
            widgets=[filter_by_preview_text, filter_preview_classes_text, classes_preview], gap=1
        )
        filter_by_size_preview_container = Container(
            widgets=[
                filter_by_preview_text,
                filter_preview_classes_text,
                classes_preview,
                area_size_preview,
                comparator_preview,
                action_preview,
            ],
            gap=1,
        )

        _settings_preview_select = Select(
            items=[
                Select.Item("names", "names", filter_by_name_preview_container),
                Select.Item("polygon_sizes", "polygon_sizes", filter_by_size_preview_container),
            ]
        )
        settings_preview = OneOf(_settings_preview_select)

        settings_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        settings_widgets_container = Container(
            widgets=[
                Field(title="Filter by", content=filter_by_select),
                filter_by_inputs,
                settings_save_btn,
            ]
        )

        saved_settings = {}

        def _set_preview():
            nonlocal saved_settings
            if "filter_by" not in saved_settings:
                return
            filter_by = saved_settings["filter_by"]
            if "names" in filter_by:
                _settings_preview_select.set_value("names")
                names = saved_settings["filter_by"]["names"]
                obj_classes = [cls for cls in classes.get_all_classes() if cls.name in names]
                classes_preview.set(obj_classes)
            else:
                _settings_preview_select.set_value("polygon_sizes")
                names = saved_settings["filter_by"]["polygon_sizes"]["filtering_classes"]
                obj_classes = [cls for cls in classes.get_all_classes() if cls.name in names]
                classes_preview.set(obj_classes)
                comparator_preview.text = (
                    f"Comparator: {saved_settings['filter_by']['polygon_sizes']['comparator']}"
                )
                action_preview.text = (
                    f"Action: {saved_settings['filter_by']['polygon_sizes']['action']}"
                )
                if "percent" in filter_by["polygon_sizes"]["area_size"]:
                    area_size_preview.text = f"Area size: {saved_settings['filter_by']['polygon_sizes']['area_size']['percent']}%"
                else:
                    area_size_preview.text = f"Area size: width = {saved_settings['filter_by']['polygon_sizes']['area_size']['width']} x height = {saved_settings['filter_by']['polygon_sizes']['area_size']['height']}"

        def _save_settings():
            nonlocal saved_settings
            settings = {}
            filter_by = filter_by_select.get_value()
            if filter_by == "names":
                settings["filter_by"] = {
                    "names": [cls.name for cls in classes.get_selected_classes()],
                }
                saved_settings = settings
            else:
                settings["filter_by"] = {
                    "polygon_sizes": {
                        "filtering_classes": [cls.name for cls in classes.get_selected_classes()],
                        "action": action_select.get_value(),
                        "comparator": comparator_select.get_value(),
                    },
                }
                if filter_by == "area_percent":
                    settings["filter_by"]["polygon_sizes"]["area_size"] = {
                        "percent": percent_input.get_value(),
                    }
                elif filter_by == "bbox_size":
                    settings["filter_by"]["polygon_sizes"]["area_size"] = {
                        "width": width_input.get_value(),
                        "height": height_input.get_value(),
                    }
                saved_settings = settings
            _set_preview()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings: dict):
            if "filter_by" not in settings:
                return
            if "names" in settings["filter_by"]:
                classes.loading = True
                filter_by_select.loading = True
                filter_by_select.set_value("names")
                classes.select(settings["filter_by"]["names"])
                filter_by_select.loading = False
                classes.loading = False
            else:
                filter_by_select.loading = True
                classes.loading = True
                comparator_select.loading = True

                if "percent" in settings["filter_by"]["polygon_sizes"]["area_size"]:
                    percent_input.loading = True
                    filter_by_select.set_value("area_percent")
                    percent_input.value = settings["filter_by"]["polygon_sizes"]["area_size"][
                        "percent"
                    ]
                else:
                    size_input.loading = True
                    filter_by_select.set_value("bbox_size")
                    width_input.value = settings["filter_by"]["polygon_sizes"]["area_size"]["width"]
                    height_input.value = settings["filter_by"]["polygon_sizes"]["area_size"][
                        "height"
                    ]
                classes.select(settings["filter_by"]["polygon_sizes"]["filtering_classes"])
                comparator_select.set_value(settings["filter_by"]["polygon_sizes"]["comparator"])

                filter_by_select.loading = False
                size_input.loading = False
                percent_input.loading = False
                classes.loading = False
                comparator_select.loading = False
            _save_settings()

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
            classes.loading = True
            classes.set(project_meta.obj_classes)
            _save_settings()
            classes.loading = False

        settings_save_btn.click(_save_settings)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Filter",
                    option_component=NodesFlow.ButtonOptionComponent(
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            settings_widgets_container
                        )
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
            meta_changed_cb=meta_changed_cb,
        )

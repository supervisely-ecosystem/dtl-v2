import copy
import os
from pathlib import Path
from typing import Optional

from supervisely.app.widgets import (
    NodesFlow,
    Switch,
    InputNumber,
    OneOf,
    Flexbox,
    Button,
    Container,
    Text,
)
from supervisely import ProjectMeta, Bitmap, AnyGeometry

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList, ClassesListPreview
from src.ui.dtl.utils import (
    classes_list_settings_changed_meta,
    get_classes_list_value,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    get_set_settings_button_style,
    get_set_settings_container,
)
import src.globals as g


class DropNoiseAction(AnnotationAction):
    name = "drop_noise"
    title = "Drop Noise"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/drop_noise_from_bitmap"
    description = "This layer (drop_noise) removes connected components smaller than the specified size from bitmap annotations. This can be useful to eliminate noise after running neural network."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes_list_widget = ClassesList(multiple=True)
        classes_list_preview = ClassesListPreview()
        save_classes_btn = Button("Save", icon="zmdi zmdi-floppy")
        set_default_classes_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        classes_list_widgets_container = Container(
            widgets=[
                classes_list_widget,
                Flexbox(
                    widgets=[
                        save_classes_btn,
                        set_default_classes_btn,
                    ],
                    gap=105,
                ),
            ]
        )
        classes_list_edit_text = Text("Classes List")
        classes_list_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        classes_list_edit_container = get_set_settings_container(
            classes_list_edit_text, classes_list_edit_btn
        )

        saved_classes_settings = []
        default_classes_settings = []

        def _get_classes_list_value():
            return get_classes_list_value(classes_list_widget, multiple=True)

        def _set_classes_list_preview():
            set_classes_list_preview(
                classes_list_widget, classes_list_preview, saved_classes_settings
            )

        def _save_classes_list_settings():
            nonlocal saved_classes_settings
            saved_classes_settings = _get_classes_list_value()

        def _set_default_classes_mapping_setting():
            # save setting to var
            nonlocal saved_classes_settings
            saved_classes_settings = copy.deepcopy(default_classes_settings)

        input_px = InputNumber(min=0)
        input_percent = InputNumber(min=0, max=100)
        px_or_percent_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=input_px,
            off_content=input_percent,
        )
        input_value = OneOf(px_or_percent_switch)
        min_area_widgets = Flexbox(widgets=[input_value, px_or_percent_switch])
        min_area_preview = Text("")
        save_min_area_btn = Button("Save", icon="zmdi zmdi-floppy")
        set_default_min_area_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        min_area_widgets_container = Container(
            widgets=[
                min_area_widgets,
                Flexbox(
                    widgets=[
                        save_min_area_btn,
                        set_default_min_area_btn,
                    ],
                    gap=105,
                ),
            ]
        )
        settings_edit_text = Text("Min Area")
        settings_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        settings_edit_container = get_set_settings_container(settings_edit_text, settings_edit_btn)

        saved_min_area_settings = "2%"
        default_min_area_settings = "2%"

        def _save_min_area_setting():
            nonlocal saved_min_area_settings
            saved_min_area_settings = _get_min_area()
            min_area_preview.text = f"Min Area: {saved_min_area_settings}"

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": saved_classes_settings,
                "min_area": saved_min_area_settings,
                "src_type": options_json["Source type"],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            classes_list_widget.loading = True
            obj_classes = [
                cls
                for cls in project_meta.obj_classes
                if cls.geometry_type in [Bitmap, AnyGeometry]
            ]

            # set classes to widget
            classes_list_widget.set(obj_classes)

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = classes_list_settings_changed_meta(
                saved_classes_settings, obj_classes
            )

            # update settings preview
            _set_classes_list_preview()

            classes_list_widget.loading = False

        def _get_min_area():
            if px_or_percent_switch.is_switched():
                return f"{input_px.value}px"
            else:
                return f"{input_percent.value}%"

        def _set_min_area(value):
            if value.endswith("px"):
                px_or_percent_switch.on()
                input_px.value = int(value[:-2])
            else:
                px_or_percent_switch.off()
                input_percent.value = int(value[:-1])

        def _set_settings_from_json(settings: dict):
            min_area_widgets.loading = True
            _set_min_area(settings.get("min_area", "2%"))
            _save_min_area_setting()
            min_area_widgets.loading = False
            classes_list_widget.loading = True
            classes_list_settings = settings.get("classes", [])
            set_classes_list_settings_from_json(
                classes_list_widget=classes_list_widget, settings=classes_list_settings
            )
            # save settings
            _save_classes_list_settings()
            # update settings preview
            _set_classes_list_preview()
            classes_list_widget.loading = False

        src_type_option_items = [
            NodesFlow.SelectOptionComponent.Item("image", "Image"),
            NodesFlow.SelectOptionComponent.Item("bbox", "Bounding Box"),
        ]

        @save_classes_btn.click
        def classes_list_save_btn_cb():
            _save_classes_list_settings()
            _set_classes_list_preview()
            g.updater("metas")

        @set_default_classes_btn.click
        def classes_list_set_default_btn_cb():
            _set_default_classes_mapping_setting()
            set_classes_list_settings_from_json(
                classes_list_widget=classes_list_widget, settings=saved_classes_settings
            )
            _set_classes_list_preview()
            g.updater("metas")

        @save_min_area_btn.click
        def save_min_area_btn_cb():
            _save_min_area_setting()
            g.updater("metas")

        @set_default_min_area_btn.click
        def set_default_min_area_btn_cb():
            _set_min_area(default_min_area_settings)
            _save_min_area_setting()
            g.updater("metas")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            src_type_val = settings.get("src_type", "image")
            settings_options = [
                NodesFlow.Node.Option(
                    name="Select Classes",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=classes_list_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_list_widgets_container
                        ),
                        sidebar_width=380,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="classes_preview_text",
                    option_component=NodesFlow.WidgetOptionComponent(classes_list_preview),
                ),
                NodesFlow.Node.Option(
                    name="Min Area",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=settings_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            min_area_widgets_container
                        ),
                        sidebar_width=380,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="min_area_preview_text",
                    option_component=NodesFlow.WidgetOptionComponent(min_area_preview),
                ),
                NodesFlow.Node.Option(
                    name="Source type",
                    option_component=NodesFlow.SelectOptionComponent(
                        items=src_type_option_items, default_value=src_type_val
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
            meta_changed_cb=meta_changed_cb,
        )

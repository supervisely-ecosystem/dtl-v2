import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta
from supervisely.app.widgets import (
    NodesFlow,
    InputNumber,
    Switch,
    Container,
    Field,
    Flexbox,
    OneOf,
    Button,
    Text,
)

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList, ClassesListPreview
from src.ui.dtl.utils import (
    classes_list_settings_changed_meta,
    get_classes_list_value,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    get_set_settings_button_style,
    get_set_settings_container,
    get_layer_docs,
    create_save_btn
)
import src.globals as g


class InstancesCropAction(SpatialLevelAction):
    name = "instances_crop"
    title = "Instances Crop"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/instances_crop"
    description = "Crops objects of specified classes from image with configurable padding."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes_list_widget = ClassesList(multiple=True)
        classes_list_preview = ClassesListPreview()
        classes_list_save_btn = create_save_btn()
        classes_list_set_default_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        classes_list_widgets_container = Container(
            widgets=[
                classes_list_widget,
                Flexbox(
                    widgets=[
                        classes_list_save_btn,
                        classes_list_set_default_btn,
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
        padding_preview = Text("")
        save_padding_btn = create_save_btn()
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
                save_padding_btn,
            ]
        )
        padding_edit_text = Text("Padding")
        padding_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        padding_edit_container = get_set_settings_container(padding_edit_text, padding_edit_btn)

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
            if "pad" not in settings:
                return
            padding = settings["pad"].get("sides", {})
            top_value = padding.get("top", "1px")
            if top_value.endswith("px"):
                padding_top_px.value = int(top_value[:-2])
                padding_top_switch.on()
            else:
                padding_top_percent.value = int(top_value[:-1])
                padding_top_switch.off()
            left_value = padding.get("left", "1px")
            if left_value.endswith("px"):
                padding_left_px.value = int(left_value[:-2])
                padding_left_switch.on()
            else:
                padding_left_percent.value = int(left_value[:-1])
                padding_left_switch.off()
            right_value = padding.get("right", "1px")
            if right_value.endswith("px"):
                padding_right_px.value = int(right_value[:-2])
                padding_right_switch.on()
            else:
                padding_right_percent.value = int(right_value[:-1])
                padding_right_switch.off()
            bot_value = padding.get("bottom", "1px")
            if bot_value.endswith("px"):
                padding_bot_px.value = int(bot_value[:-2])
                padding_bot_switch.on()
            else:
                padding_bot_percent.value = int(bot_value[:-1])
                padding_bot_switch.off()

        saved_padding_settings = {}

        def _save_padding():
            nonlocal saved_padding_settings
            saved_padding_settings = _get_padding()
            padding_preview.text = f'Top: {saved_padding_settings["sides"]["top"]} Left: {saved_padding_settings["sides"]["left"]} Right: {saved_padding_settings["sides"]["right"]} Bottom: {saved_padding_settings["sides"]["bottom"]}'

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": saved_classes_settings,
                "pad": saved_padding_settings,
            }

        def _set_settings_from_json(settings: dict):
            padding_container.loading = True
            _set_padding(settings)
            _save_padding()
            padding_container.loading = False
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

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            classes_list_widget.loading = True
            obj_classes = [cls for cls in project_meta.obj_classes]

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

        save_padding_btn.click(_save_padding)

        @classes_list_save_btn.click
        def classes_list_save_btn_cb():
            _save_classes_list_settings()
            _set_classes_list_preview()
            g.updater("metas")

        @classes_list_set_default_btn.click
        def classes_list_set_default_btn_cb():
            _set_default_classes_mapping_setting()
            set_classes_list_settings_from_json(
                classes_list_widget=classes_list_widget, settings=saved_classes_settings
            )
            _set_classes_list_preview()
            g.updater("metas")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
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
                    name="classes_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_list_preview),
                ),
                NodesFlow.Node.Option(
                    name="Set Padding",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=padding_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(padding_container),
                        sidebar_width=300,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="padding_preview",
                    option_component=NodesFlow.WidgetOptionComponent(padding_preview),
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

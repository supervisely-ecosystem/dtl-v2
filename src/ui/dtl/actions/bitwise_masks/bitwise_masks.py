import copy
from typing import Optional

from supervisely.app.widgets import NodesFlow, Button, Container, Flexbox, Text
from supervisely import ProjectMeta

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
    get_layer_docs
)
from src.exceptions import BadSettingsError
import src.globals as g


class BitwiseMasksAction(AnnotationAction):
    name = "bitwise_masks"
    title = "Bitwise Masks"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bitwise_masks"
    )
    description = "Make bitwise operations between bitmap annotations."
    md_description = get_layer_docs()

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        class_mask_widget = ClassesList()
        classes_to_correct_widget = ClassesList(multiple=True)

        class_mask_preview = ClassesListPreview()
        classes_to_correct_preview = ClassesListPreview()

        save_class_mask_btn = Button("Save", icon="zmdi zmdi-floppy")
        save_classes_to_correct_btn = Button("Save", icon="zmdi zmdi-floppy")

        set_default_class_mask_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        set_default_classes_to_correct_btn = Button("Set Default", icon="zmdi zmdi-refresh")

        class_mask_widgets_container = Container(
            widgets=[
                class_mask_widget,
                Flexbox(
                    widgets=[
                        save_class_mask_btn,
                        set_default_class_mask_btn,
                    ],
                    gap=105,
                ),
            ]
        )
        classes_to_correct_widgets_container = Container(
            widgets=[
                classes_to_correct_widget,
                Flexbox(
                    widgets=[
                        save_classes_to_correct_btn,
                        set_default_classes_to_correct_btn,
                    ],
                    gap=105,
                ),
            ]
        )
        class_mask_edit_text = Text("Class Mask. First element of bitwise operation")
        class_mask_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        class_mask_edit_container = get_set_settings_container(
            class_mask_edit_text, class_mask_edit_btn
        )
        classes_to_correct_edit_text = Text("Classes to correct")
        classes_to_correct_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        classes_to_correct_edit_container = get_set_settings_container(
            classes_to_correct_edit_text, classes_to_correct_edit_btn
        )

        saved_class_mask_settings = ""
        saved_classes_to_correct_settings = []

        default_class_mask_settings = ""
        default_classes_to_correct_settings = []

        def _get_class_mask_value():
            return get_classes_list_value(class_mask_widget, multiple=False)

        def _set_class_mask_preview():
            set_classes_list_preview(
                class_mask_widget, class_mask_preview, saved_class_mask_settings
            )

        def _save_class_mask_settings():
            nonlocal saved_class_mask_settings
            saved_class_mask_settings = _get_class_mask_value()

        def _set_default_class_mask_setting():
            # save setting to var
            nonlocal saved_class_mask_settings
            saved_class_mask_settings = copy.deepcopy(default_class_mask_settings)

        def _get_classes_to_correct_value():
            return get_classes_list_value(classes_to_correct_widget, multiple=True)

        def _set_classes_to_correct_preview():
            set_classes_list_preview(
                classes_to_correct_widget,
                classes_to_correct_preview,
                saved_classes_to_correct_settings,
            )

        def _save_classes_to_correct_settings():
            nonlocal saved_classes_to_correct_settings
            saved_classes_to_correct_settings = _get_classes_to_correct_value()

        def _set_default_classes_to_correct_setting():
            # save setting to var
            nonlocal saved_classes_to_correct_settings
            saved_classes_to_correct_settings = copy.deepcopy(default_classes_to_correct_settings)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "type": options_json["type"],
                "class_mask": saved_class_mask_settings,
                "classes_to_correct": saved_classes_to_correct_settings,
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            class_mask_widget.loading = True
            obj_classes = [cls for cls in project_meta.obj_classes]
            # set classes to widget
            class_mask_widget.set(obj_classes)
            # update settings according to new meta
            nonlocal saved_class_mask_settings
            saved_class_mask_settings = classes_list_settings_changed_meta(
                saved_class_mask_settings, obj_classes
            )
            # update settings preview
            _set_class_mask_preview()
            class_mask_widget.loading = False

            classes_to_correct_widget.loading = True
            obj_classes = [cls for cls in project_meta.obj_classes]
            # set classes to widget
            classes_to_correct_widget.set(obj_classes)
            # update settings according to new meta
            nonlocal saved_classes_to_correct_settings
            saved_classes_to_correct_settings = classes_list_settings_changed_meta(
                saved_classes_to_correct_settings, obj_classes
            )
            # update settings preview
            _set_classes_to_correct_preview()
            classes_to_correct_widget.loading = False

        def _set_settings_from_json(settings):
            class_mask_widget.loading = True
            classes_list_settings = settings.get("class_mask", "")
            set_classes_list_settings_from_json(
                classes_list_widget=class_mask_widget, settings=classes_list_settings
            )
            # save settings
            _save_class_mask_settings()
            # update settings preview
            _set_class_mask_preview()
            class_mask_widget.loading = False

            classes_to_correct_widget.loading = True
            classes_list_settings = settings.get("classes_to_correct", [])
            set_classes_list_settings_from_json(
                classes_list_widget=classes_to_correct_widget, settings=classes_list_settings
            )
            # save settings
            _save_classes_to_correct_settings()
            # update settings preview
            _set_classes_to_correct_preview()
            classes_to_correct_widget.loading = False

        @save_class_mask_btn.click
        def save_class_mask_btn_cb():
            _save_class_mask_settings()
            _set_class_mask_preview()
            g.updater("metas")

        @set_default_class_mask_btn.click
        def set_default_class_mask_btn_cb():
            _set_default_class_mask_setting()
            set_classes_list_settings_from_json(
                classes_list_widget=class_mask_widget, settings=saved_class_mask_settings
            )
            _set_class_mask_preview()
            g.updater("metas")

        @save_classes_to_correct_btn.click
        def save_classes_to_correct_btn_cb():
            _save_classes_to_correct_settings()
            _set_classes_to_correct_preview()
            g.updater("metas")

        @set_default_classes_to_correct_btn.click
        def set_default_classes_to_correct_btn_cb():
            _set_default_classes_to_correct_setting()
            set_classes_list_settings_from_json(
                classes_list_widget=classes_to_correct_widget,
                settings=saved_classes_to_correct_settings,
            )
            _set_classes_to_correct_preview()
            g.updater("metas")

        type_items = [NodesFlow.SelectOptionComponent.Item(t, t) for t in ("nor", "and", "or")]

        def create_options(src: list, dst: list, settings: dict) -> dict:
            type_val = settings.get("type", "nor")
            if type_val not in ("nor", "and", "or"):
                raise BadSettingsError("Type must be one of: nor, and, or")

            _set_settings_from_json(settings)

            settings_options = [
                NodesFlow.Node.Option(
                    name="type_text",
                    option_component=NodesFlow.TextOptionComponent("Operation type"),
                ),
                NodesFlow.Node.Option(
                    name="type",
                    option_component=NodesFlow.SelectOptionComponent(
                        items=type_items, default_value=type_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Select Class Mask",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=class_mask_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            class_mask_widgets_container
                        ),
                        sidebar_width=380,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="class_mask_preview",
                    option_component=NodesFlow.WidgetOptionComponent(class_mask_preview),
                ),
                NodesFlow.Node.Option(
                    name="Select Classes to correct",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=classes_to_correct_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_to_correct_widgets_container
                        ),
                        sidebar_width=380,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="classes_to_correct_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_to_correct_preview),
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

from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta
from supervisely.app.widgets import NodesFlow

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

from src.ui.dtl.actions.annotation_transforms.objects_filter_by_area.layout.objects_filter_by_area_layout import (
    create_layout_widgets,
)

from src.ui.dtl.actions.annotation_transforms.objects_filter_by_area.layout.objects_filter_by_area_sidebar import (
    create_sidebar_widgets,
)


# @TODO: Disable add_tag option if no tags are available in project meta
# @TODO: Hide settings preview until selected


class ObjectsFilterByAreaAction(AnnotationAction):
    name = "objects_filter_by_area"
    title = "Objects Filter by Area"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/objects_filter_by_area"
    description = "Select one of the actions to apply to filtered objects: delete, add tag"
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        saved_settings = {}

        (
            # Layout
            layout_edit_text,
            layout_edit_btn,
            layout_edit_container,
            # Preview
            layout_classes_preview_text,
            layout_classes_preview,
            layout_classes_preview_container,
            layout_preview_area,
            layout_preview_action,
            layout_preview_condition,
            layout_tags_preview_text,
            layout_preview_tags,
            layout_preview_container,
        ) = create_layout_widgets()

        (
            # Sidebar Classes
            sidebar_classes,
            sidebar_classes_field,
            # Sidebar Area
            sidebar_area_input,
            sidebar_area_input_field,
            # Sidebar Comparator
            sidebar_comparator_select,
            sidebar_comparator_select_field,
            # Sidebar Action
            sidebar_action_select,
            sidebar_action_select_field,
            # Sidebar Tags
            sidebar_tags,
            sidebar_tags_field,
            # Sidebar Save button
            sidebar_save_btn,
            # Sidebar
            sidebar_container,
        ) = create_sidebar_widgets()

        # Sidebar CB
        @sidebar_save_btn.click
        def sidebar_save_btn_cb():
            _save_settings()
            # layout_preview_area.show()
            # layout_preview_action.show()
            # layout_preview_condition.show()
            # layout_tags_preview_text.show()
            # layout_preview_tags.show()
            # layout_preview_container.show()

        @sidebar_action_select.value_changed
        def sidebar_action_select_cb(value):
            if value == "add_tags":
                sidebar_tags_field.show()
            else:
                sidebar_tags_field.hide()

        # --------------------------------

        def data_changed_cb(**kwargs):
            project_meta = kwargs.get("project_meta", None)
            if project_meta is None:
                return
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
            sidebar_classes.loading = True
            sidebar_classes.set(project_meta.obj_classes)
            sidebar_classes.loading = False

            sidebar_tags.loading = True
            sidebar_tags.set(project_meta.tag_metas)
            sidebar_tags.loading = False
            _save_settings()

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_settings
            return saved_settings

        def _set_preview():
            classes = sidebar_classes.get_selected_classes()
            area = sidebar_area_input.get_value()
            comparator = sidebar_comparator_select.get_label()
            action = sidebar_action_select.get_value()
            action_label = sidebar_action_select.get_label()

            layout_classes_preview_text.text = (
                f"Classes: {len(classes)} / {len(_current_meta.obj_classes)}"
            )
            layout_classes_preview.set(classes)
            layout_preview_area.text = f"Area size: {area} px"
            layout_preview_area.show()
            layout_preview_action.text = f"Action: {action_label}"
            layout_preview_action.show()
            layout_preview_condition.text = f"Condition: {comparator}"
            layout_preview_condition.show()

            if action == "add_tags":
                tags = sidebar_tags.get_selected_tag_metas()
                layout_tags_preview_text.text = (
                    f"Tags: {len(tags)} / {len(_current_meta.tag_metas)}"
                )
                layout_tags_preview_text.show()
                layout_preview_tags.show()
            else:
                tags = []
                layout_tags_preview_text.hide()
                layout_preview_tags.hide()
            layout_preview_tags.set(tags)

        def _save_settings():
            nonlocal saved_settings
            classes = sidebar_classes.get_selected_classes()
            classes_names = [obj_cls.name for obj_cls in classes]
            area = sidebar_area_input.get_value()
            comparator = sidebar_comparator_select.get_value()
            action = sidebar_action_select.get_value()
            if action == "add_tags":
                tags = sidebar_tags.get_selected_tags()
                tags = [{"name": tag.name, "value": tag.value} for tag in tags]
            else:
                tags = []

            saved_settings = {
                "classes": classes_names,
                "area": area,
                "comparator": comparator,
                "action": action,
                "tags_to_add": tags,
            }
            _set_preview()

        def _set_settings_from_json(settings: dict):
            classes = settings.get("classes", [])
            sidebar_classes.select(classes)
            area = settings.get("area", 100)
            sidebar_area_input.value = area
            comparator = settings.get("comparator", "gt")
            sidebar_comparator_select.set_value(comparator)
            action = settings.get("action", "delete")
            sidebar_action_select.set_value(action)
            if action == "add_tags":
                tags = settings.get("tags_to_add", [])
                tag_names = [tag["name"] for tag in tags]
                sidebar_tags.select(tag_names)
                tag_values_map = {tag["name"]: tag["value"] for tag in tags}
                sidebar_tags.set_values(tag_values_map)
                sidebar_tags_field.show()
            else:
                sidebar_tags.select([])
            _save_settings()

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Settings",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=layout_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(sidebar_container),
                        sidebar_width=300,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Classes Preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        layout_classes_preview_container
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Settings Preview",
                    option_component=NodesFlow.WidgetOptionComponent(layout_preview_container),
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
            data_changed_cb=data_changed_cb,
            need_preview=True,
        )

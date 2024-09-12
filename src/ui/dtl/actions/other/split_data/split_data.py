from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

from supervisely.app.widgets import NodesFlow
from src.ui.dtl.actions.other.split_data.layout.split_data_sidebar import create_sidebar_widgets
from src.ui.dtl.actions.other.split_data.layout.split_data_layout import create_layout_widgets
from supervisely import ProjectMeta


class SplitDataAction(OtherAction):
    name = "split_data"
    title = "Split Data"
    docs_url = ""
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        (
            sidebar_selector,
            sidebar_selector_field,
            sidebar_percent_field,
            sidebar_number_field,
            sidebar_classes,
            sidebar_classes_field,
            sidebar_tags,
            sidebar_tags_field,
            sidebar_container,
        ) = create_sidebar_widgets()

        layout_text, layout_edit_button, layout_container, layout_current_method = (
            create_layout_widgets()
        )
        layout_current_method.set(f"Current method: {sidebar_selector.get_label()}", "text")
        sidebar_percent_field.show()

        @sidebar_selector.value_changed
        def selector_cb(value):
            layout_current_method.set(f"Current method: {sidebar_selector.get_label()}", "text")
            if value == 0:
                sidebar_percent_field.show()
                sidebar_number_field.hide()
                sidebar_classes_field.hide()
                sidebar_tags_field.hide()
            elif value == 1:
                sidebar_percent_field.hide()
                sidebar_number_field.show()
                sidebar_classes_field.hide()
                sidebar_tags_field.hide()
            elif value == 2:
                sidebar_percent_field.hide()
                sidebar_number_field.hide()
                sidebar_classes_field.show()
                sidebar_tags_field.hide()
            elif value == 3:
                sidebar_percent_field.hide()
                sidebar_number_field.hide()
                sidebar_classes_field.hide()
                sidebar_tags_field.show()

        def get_settings(options_json: dict) -> dict:
            return {"method": sidebar_selector.get_value()}

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

        def create_options(src: list, dst: list, settings: dict) -> dict:
            settings_options = [
                NodesFlow.Node.Option(
                    name="Layout",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(sidebar_container),
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
            data_changed_cb=data_changed_cb,
            need_preview=False,
        )

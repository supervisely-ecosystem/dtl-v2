from typing import Optional
from os.path import realpath, dirname
from supervisely.app.widgets import ProjectThumbnail, NodesFlow, Text, Button, Container, FastTable
from supervisely import ProjectMeta

from src.ui.dtl import SourceAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs
import src.globals as g
from src.ui.widgets import ClassesListPreview, TagsListPreview
from src.ui.dtl.utils import (
    get_text_font_size,
    get_layer_docs,
    get_set_settings_button_style,
    get_set_settings_container,
)
from src.ui.dtl.actions.input.filtered_project.utils import build_filtered_table


class FilteredProjectAction(SourceAction):
    name = "filtered_project"
    title = "Filtered Project"
    docs_url = ""
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_inputs(self):
        return []

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        # Settings widgets
        _current_info = g.api.project.get_info_by_id(g.PROJECT_ID)
        _current_meta: ProjectMeta = ProjectMeta.from_json(g.api.project.get_meta(g.PROJECT_ID))

        filtered_table_data = build_filtered_table(g.api, g.PROJECT_ID, g.FILTERED_ITEMS_IDS)
        filtered_table = FastTable(data=filtered_table_data)
        filtered_data_btn = Button(
            "Continue", icon="zmdi zmdi-floppy", call_on_click="closeSidebar();"
        )

        filtered_data_container = Container([filtered_table, filtered_data_btn])

        filtered_project_preview = ProjectThumbnail(_current_info)
        show_filtered_data_btn = Button(
            text="SHOW",
            icon="zmdi zmdi-folder",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        show_data_container = get_set_settings_container(
            filtered_project_preview, show_filtered_data_btn
        )

        classes_preview_text = Text(
            f"Classes {len(_current_meta.obj_classes)} / {len(_current_meta.obj_classes)}"
        )
        classes_preview = ClassesListPreview()
        classes_preview.set([obj_class for obj_class in _current_meta.obj_classes])

        tags_preview_text = Text(
            f"Tags {len(_current_meta.tag_metas)} / {len(_current_meta.tag_metas)}"
        )
        tags_preview = TagsListPreview([obj_class for obj_class in _current_meta.tag_metas])

        # def data_changed_cb(**kwargs):
        #     nonlocal _current_info, _current_meta
        #     classes_preview.set(_current_meta.obj_classes)
        #     tags_preview.set(_current_meta.tag_metas)

        def get_settings(options_json: dict) -> dict:
            return {}

        def create_options(src: list, dst: list, settings: dict) -> dict:
            src_options = [
                NodesFlow.Node.Option(
                    name="Source Preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=show_data_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(filtered_data_container),
                        sidebar_width=300,
                    ),
                ),
            ]
            settings_options = [
                NodesFlow.Node.Option(
                    name="Classes Preview Text",
                    option_component=NodesFlow.WidgetOptionComponent(classes_preview_text),
                ),
                NodesFlow.Node.Option(
                    name="Classes Preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_preview),
                ),
                NodesFlow.Node.Option(
                    name="Tags Preview Text",
                    option_component=NodesFlow.WidgetOptionComponent(tags_preview_text),
                ),
                NodesFlow.Node.Option(
                    name="Tags Preview",
                    option_component=NodesFlow.WidgetOptionComponent(tags_preview),
                ),
            ]

            return {
                "src": src_options,
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=True,
        )

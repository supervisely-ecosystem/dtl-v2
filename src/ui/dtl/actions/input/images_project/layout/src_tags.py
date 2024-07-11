import copy
from os.path import dirname, realpath
from typing import List, Optional

import src.globals as g
import src.utils as utils
from src.ui.dtl import SourceAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    create_save_btn,
    get_text_font_size,
    get_layer_docs,
    mapping_to_list,
    get_set_settings_button_style,
    get_set_settings_container,
    # classes
    classes_list_to_mapping,
    get_classes_list_value,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    classes_list_settings_changed_meta,
    # tags
    tags_list_to_mapping,
    get_tags_list_value,
    set_tags_list_preview,
    set_tags_list_settings_from_json,
    tags_list_settings_changed_meta,
)
from src.ui.widgets import ClassesListPreview, TagsListPreview
from supervisely import ProjectMeta, ProjectType
from supervisely.app.content import StateJson
from supervisely.app.widgets import (
    Button,
    Container,
    NodesFlow,
    NotificationBox,
    SelectDataset,
    Text,
    ClassesTable,
    TagsTable,
    ProjectThumbnail,
    Field,
)


def create_tags_selector_widgets():
    tags_mapping_widget = TagsTable()
    tags_mapping_save_btn = create_save_btn()
    tags_mapping_set_default_btn = Button(
        "Set Default", button_type="info", plain=True, icon="zmdi zmdi-refresh"
    )
    tags_mapping_preview = TagsListPreview()

    tags_mapping_field = Field(
        content=tags_mapping_widget,
        title="Tags",
        description=(
            "Select tags that will be used in data transformation processes. "
            "If tag is not selected, it will be ignored."
        ),
    )
    tags_mapping_widgets_container = Container(
        widgets=[
            tags_mapping_field,
            Container(
                widgets=[
                    tags_mapping_save_btn,
                    tags_mapping_set_default_btn,
                ],
                direction="horizontal",
                gap=0,
                fractions=[1, 0],
                # gap=355,
            ),
        ]
    )
    tags_mapping_edit_text = Text("Tags", status="text", font_size=get_text_font_size())
    tags_mapping_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )

    if g.PROJECT_ID is None:
        tags_mapping_edit_btn.disable()

    tags_mapping_edit_contaniner = get_set_settings_container(
        tags_mapping_edit_text, tags_mapping_edit_btn
    )

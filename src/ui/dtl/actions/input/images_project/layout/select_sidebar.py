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
    DatasetThumbnail,
    Field,
)


def set_current_src_context(dataset_selector_widget: SelectDataset):
    # fix team and workspace for SelectDataset widget
    StateJson()[dataset_selector_widget._project_selector._ws_selector._team_selector.widget_id][
        "teamId"
    ] = g.TEAM_ID
    StateJson()[dataset_selector_widget._project_selector._ws_selector.widget_id][
        "workspaceId"
    ] = g.WORKSPACE_ID
    dataset_selector_widget._project_selector._ws_selector.disable()
    StateJson().send_changes()


def create_project_sidebar_widgets():
    # Sidebar
    src_sidebar_dataset_selector = SelectDataset(
        multiselect=True,
        select_all_datasets=True,
        allowed_project_types=[ProjectType.IMAGES],
        compact=False,
    )
    set_current_src_context(src_sidebar_dataset_selector)

    src_sidebar_save_btn = Button(
        "Save", icon="zmdi zmdi-floppy", emit_on_click="save", call_on_click="closeSidebar();"
    )
    src_sidebar_empty_dataset_notification = NotificationBox(
        title="No datasets selected", description="Select at lease one dataset"
    )
    src_sidebar_empty_dataset_notification.hide()
    src_sidebar_widgets_container = Container(
        widgets=[
            src_sidebar_dataset_selector,
            src_sidebar_empty_dataset_notification,
            src_sidebar_save_btn,
        ]
    )
    # Preview

    src_sidebar_preview_widget_text = Text("", status="text", font_size=get_text_font_size())
    src_sidebar_preview_widget_text.hide()

    # If Multiple datasets
    src_sidebar_preview_widget_pr_thumbnail = ProjectThumbnail(remove_margins=True)
    src_sidebar_preview_widget_pr_thumbnail.hide()
    # If Single dataset
    src_sidebar_preview_widget_ds_thumbnail = DatasetThumbnail(remove_margins=True)
    src_sidebar_preview_widget_ds_thumbnail.hide()

    src_sidebar_preview_widget = Container(
        widgets=[
            src_sidebar_preview_widget_pr_thumbnail,
            src_sidebar_preview_widget_ds_thumbnail,
            src_sidebar_preview_widget_text,
        ]
    )

    # Layout
    src_sidebar_layout_text = Text("Select Project", status="text", font_size=get_text_font_size())
    src_sidebar_layout_select_btn = Button(
        text="SELECT",
        icon="zmdi zmdi-folder",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    src_sidebar_layout_container = get_set_settings_container(
        src_sidebar_layout_text, src_sidebar_layout_select_btn
    )

    return (
        # Sidebar
        src_sidebar_dataset_selector,
        src_sidebar_save_btn,
        src_sidebar_empty_dataset_notification,
        src_sidebar_widgets_container,
        # Preview
        src_sidebar_preview_widget_text,
        src_sidebar_preview_widget_pr_thumbnail,
        src_sidebar_preview_widget_ds_thumbnail,
        src_sidebar_preview_widget,
        # Layout
        src_sidebar_layout_text,
        src_sidebar_layout_select_btn,
        src_sidebar_layout_container,
    )

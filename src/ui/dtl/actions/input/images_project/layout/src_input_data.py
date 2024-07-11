import src.globals as g
from src.ui.dtl.utils import (
    create_save_btn,
    get_text_font_size,
    get_set_settings_button_style,
    get_set_settings_container,
)
from supervisely import ProjectType
from supervisely.app.content import StateJson
from supervisely.app.widgets import (
    Button,
    Container,
    NotificationBox,
    SelectDataset,
    Text,
    ProjectThumbnail,
    DatasetThumbnail,
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


def create_input_data_selector_widgets():
    # Sidebar
    src_input_data_sidebar_dataset_selector = SelectDataset(
        multiselect=True,
        select_all_datasets=True,
        allowed_project_types=[ProjectType.IMAGES],
        compact=False,
    )
    set_current_src_context(src_input_data_sidebar_dataset_selector)
    src_input_data_sidebar_save_btn = create_save_btn()
    src_input_data_sidebar_empty_ds_notification = NotificationBox(
        title="No datasets selected", description="Select at lease one dataset"
    )
    src_input_data_sidebar_empty_ds_notification.hide()
    src_input_data_sidebar_widgets_container = Container(
        widgets=[
            src_input_data_sidebar_dataset_selector,
            src_input_data_sidebar_empty_ds_notification,
            src_input_data_sidebar_save_btn,
        ]
    )
    # Preview

    src_input_data_sidebar_preview_widget_text = Text(
        "", status="text", font_size=get_text_font_size()
    )
    src_input_data_sidebar_preview_widget_text.hide()

    # If Multiple datasets
    src_input_data_sidebar_preview_widget_pr_thumbnail = ProjectThumbnail(remove_margins=True)
    src_input_data_sidebar_preview_widget_pr_thumbnail.hide()
    # If Single dataset
    src_input_data_sidebar_preview_widget_ds_thumbnail = DatasetThumbnail(remove_margins=True)
    src_input_data_sidebar_preview_widget_ds_thumbnail.hide()

    src_input_data_sidebar_preview_widget = Container(
        widgets=[
            src_input_data_sidebar_preview_widget_pr_thumbnail,
            src_input_data_sidebar_preview_widget_ds_thumbnail,
            src_input_data_sidebar_preview_widget_text,
        ]
    )

    # Layout
    src_input_data_sidebar_layout_text = Text(
        "Select Project", status="text", font_size=get_text_font_size()
    )
    src_input_data_sidebar_layout_select_btn = Button(
        text="SELECT",
        icon="zmdi zmdi-folder",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    src_input_data_sidebar_layout_container = get_set_settings_container(
        src_input_data_sidebar_layout_text, src_input_data_sidebar_layout_select_btn
    )

    return (
        # Sidebar
        src_input_data_sidebar_dataset_selector,
        src_input_data_sidebar_save_btn,
        src_input_data_sidebar_empty_ds_notification,
        src_input_data_sidebar_widgets_container,
        # Preview
        src_input_data_sidebar_preview_widget_text,
        src_input_data_sidebar_preview_widget_pr_thumbnail,
        src_input_data_sidebar_preview_widget_ds_thumbnail,
        src_input_data_sidebar_preview_widget,
        # Layout
        src_input_data_sidebar_layout_text,
        src_input_data_sidebar_layout_select_btn,
        src_input_data_sidebar_layout_container,
    )

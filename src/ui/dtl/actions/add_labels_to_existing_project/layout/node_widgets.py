import src.globals as g
from src.ui.dtl.utils import (
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
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
    Field,
    Select,
    Checkbox,
)


def create_node_widgets():
    # PROJECT SELECTOR
    # SIDEBAR
    select_project_sidebar_dataset_selector = SelectDataset(
        multiselect=True,
        select_all_datasets=True,
        allowed_project_types=[ProjectType.IMAGES],
        compact=False,
    )

    select_project_sidebar_dataset_selector_field = Field(
        title="Select destination project or dataset",
        description="If multiple datasets are selected, labels only from the datasets with the same names from input project will be added",
        content=select_project_sidebar_dataset_selector,
    )

    # fix team and workspace for SelectDataset widget
    StateJson()[
        select_project_sidebar_dataset_selector._project_selector._ws_selector._team_selector.widget_id
    ]["teamId"] = g.TEAM_ID
    StateJson()[select_project_sidebar_dataset_selector._project_selector._ws_selector.widget_id][
        "workspaceId"
    ] = g.WORKSPACE_ID
    select_project_sidebar_dataset_selector._project_selector._ws_selector.disable()
    StateJson().send_changes()

    select_project_sidebar_empty_dataset_notification = NotificationBox(
        title="No datasets selected", description="Select at lease one dataset"
    )
    select_project_sidebar_empty_dataset_notification.hide()

    select_project_sidebar_save_btn = create_save_btn()

    select_project_sidebar_container = Container(
        widgets=[
            select_project_sidebar_dataset_selector,
            select_project_sidebar_empty_dataset_notification,
            select_project_sidebar_save_btn,
        ]
    )
    # PREVIEW
    select_project_preview_text = Text("", status="text", font_size=get_text_font_size())
    select_project_preview_text.hide()
    select_project_preview_thumbnail = ProjectThumbnail(remove_margins=True)
    select_project_preview_thumbnail.hide()
    select_project_preview_container = Container(
        widgets=[select_project_preview_thumbnail, select_project_preview_text]
    )

    # LAYOUT
    select_project_edit_text = Text("Select Project", status="text", font_size=get_text_font_size())
    select_project_edit_btn = Button(
        text="SELECT",
        icon="zmdi zmdi-folder",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    select_project_edit_container = get_set_settings_container(
        select_project_edit_text, select_project_edit_btn
    )
    # -----------------------------

    # SELECT OPTION
    select_option_items = [Select.Item("merge", "Merge"), Select.Item("replace", "Replace")]
    select_option = Select(items=select_option_items, size="small")
    select_option_field = Field(
        title="Select how to add labels",
        description="Option 'Merge' will add labels to the existing ones, option 'Replace' will remove the existing labels and add new ones",
        content=select_option,
    )
    # -----------------------------

    # BACKUP DESTINATION
    backup_target_project_checkbox = Checkbox("Backup selected project", True)
    backup_target_project_notification = NotificationBox(
        title="Selected project will be modified",
        description="If you want to backup this project, check the box above",
        box_type="warning",
    )
    backup_target_project_notification.hide()

    # -----------------------------

    return (
        # project selector
        # sidebar
        select_project_sidebar_dataset_selector,
        select_project_sidebar_dataset_selector_field,
        select_project_sidebar_empty_dataset_notification,
        select_project_sidebar_save_btn,
        select_project_sidebar_container,
        # preview
        select_project_preview_text,
        select_project_preview_thumbnail,
        select_project_preview_container,
        # layout
        select_project_edit_text,
        select_project_edit_btn,
        select_project_edit_container,
        # select option
        select_option,
        select_option_field,
        # backup destination
        backup_target_project_checkbox,
        backup_target_project_notification,
    )

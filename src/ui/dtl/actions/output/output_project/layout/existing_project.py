import src.globals as g
from supervisely.app.widgets import (
    Text,
    Select,
    SelectProject,
    SelectDatasetTree,
    Button,
    Container,
    Input,
    ProjectThumbnail,
    Field,
    OneOf,
    Empty,
    Checkbox,
    NotificationBox,
)

from supervisely.app.content import StateJson
from src.ui.dtl.utils import (
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
    create_save_btn,
)
from src.ui.dtl.utils import get_layer_docs, get_text_font_size


def create_existing_project_widgets():
    # SIDEBAR
    dst_project_selector = SelectProject(
        workspace_id=g.WORKSPACE_ID,
        allowed_types=[g.SUPPORTED_MODALITIES_MAP[g.MODALITY_TYPE]],
        size="small",
    )

    # fix team and workspace for SelectProject widget
    StateJson()[dst_project_selector._ws_selector._team_selector.widget_id]["teamId"] = g.TEAM_ID
    StateJson()[dst_project_selector._ws_selector.widget_id]["workspaceId"] = g.WORKSPACE_ID
    dst_project_selector._ws_selector.disable()
    StateJson().send_changes()

    dst_project_selector_field = Field(
        title="Select Destination Project",
        description="Results will be saved to selected project.",
        content=dst_project_selector,
    )

    dst_dataset_options_existing_dataset_selector = SelectDatasetTree(
        multiselect=False,
        flat=True,
        select_all_datasets=False,
        allowed_project_types=[g.SUPPORTED_MODALITIES_MAP[g.MODALITY_TYPE]],
        always_open=False,
        compact=True,
        team_is_selectable=False,
        workspace_is_selectable=False,
        append_to_body=False,
    )

    dst_dataset_options_new_dataset_input = Input(placeholder="Enter dataset name", size="small")

    dst_dataset_options_selector_items = [
        Select.Item("new", "New Dataset", dst_dataset_options_new_dataset_input),
        Select.Item("existing", "Existing Dataset", dst_dataset_options_existing_dataset_selector),
        Select.Item("keep", "Keep source structure", Empty()),
    ]
    dst_dataset_options_selector = Select(dst_dataset_options_selector_items, size="small")
    dst_dataset_options_selector_oneof = OneOf(dst_dataset_options_selector)
    dst_dataset_options_selector_text_1 = Text(
        text=(" - Existing Dataset: select dataset from existing project to save results to."),
        color="#7f858e",
        font_size=13,
    )
    dst_dataset_options_selector_text_2 = Text(
        text=(" - New Dataset: enter name of new dataset to create in selected existing project."),
        color="#7f858e",
        font_size=13,
    )
    dst_dataset_options_selector_text_3 = Text(
        text=(
            " - Keep source structure: save the results in datasets that repeats the structure of the input project."
        ),
        color="#7f858e",
        font_size=13,
    )
    dst_dataset_options_selector_field = Field(
        title="Select Dataset Options",
        content=Container(
            [
                dst_dataset_options_selector_text_1,
                dst_dataset_options_selector_text_2,
                dst_dataset_options_selector_text_3,
                dst_dataset_options_selector,
                dst_dataset_options_selector_oneof,
            ]
        ),
    )

    sidebar_save_button = create_save_btn()

    select_project_warning_notification_box = NotificationBox(
        box_type="warning",
        description=(
            "The ProjectMeta of the source project does not match the ProjectMeta of the destination project. "
            "By ticking this checkbox, you confirm that you understand "
            "and approve the update of the destination project's ProjectMeta."
        ),
    )
    select_project_warning_checkbox = Checkbox("Confirm")
    select_project_warning_container = Container(
        [select_project_warning_notification_box, select_project_warning_checkbox]
    )
    select_project_warning_container.hide()

    sidebar_container = Container(
        [
            dst_project_selector_field,
            dst_dataset_options_selector_field,
            sidebar_save_button,
        ]
    )

    # LAYOUT
    select_project_text = Text("Select Project", status="text", font_size=get_text_font_size())
    select_project_btn = Button(
        text="SELECT",
        icon="zmdi zmdi-folder",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    select_project_container = get_set_settings_container(select_project_text, select_project_btn)

    # PREVIEW
    dst_project_preview = ProjectThumbnail()
    dst_project_preview_warning = Text(
        f"Project does not exist in the current workspace (ID: {g.WORKSPACE_ID})",
        "error",
        font_size=get_text_font_size(),
    )
    dst_project_preview_warning.hide()
    dst_dataset_preview = Text("", "text", font_size=get_text_font_size())
    dst_preview_container = Container(
        [dst_project_preview, dst_project_preview_warning, dst_dataset_preview]
    )
    dst_preview_container.hide()

    return (
        # SIDEBAR
        dst_project_selector,
        dst_dataset_options_existing_dataset_selector,
        dst_dataset_options_new_dataset_input,
        dst_dataset_options_selector,
        sidebar_save_button,
        select_project_warning_checkbox,
        select_project_warning_container,
        sidebar_container,
        # LAYOUT
        select_project_container,
        # PREVIEW
        dst_project_preview,
        dst_project_preview_warning,
        dst_dataset_preview,
        dst_preview_container,
    )

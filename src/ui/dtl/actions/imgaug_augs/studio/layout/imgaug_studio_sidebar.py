from supervisely.app.widgets import (
    Container,
    Button,
    Field,
    Select,
    Input,
    Text,
    FileThumbnail,
)
from supervisely import env
from src.ui.widgets.augs_list import AugsList
from src.ui.widgets.augs_list_params_selector import AugsListParamsSelector
from src.ui.dtl.utils import create_save_btn
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as aug_utils


def create_sidebar_widgets():
    # Sidebar Initialization widgets
    sidebar_init_items = [
        Select.Item(0, "start from scratch"),
        Select.Item(1, "load augs from existing pipeline"),
    ]
    sidebar_init_selector = Select(sidebar_init_items)
    team_files_url = f"{env.server_address().rstrip('/')}/files/"
    sidebar_team_files_link_btn = Button(
        text="Open Team Files",
        button_type="info",
        plain=True,
        icon="zmdi zmdi-folder",
        link=team_files_url,
    )
    sidebar_team_files_link_btn.hide()
    sidebar_init_input = Input(placeholder="Please input path to json configuration in Team Files")
    sidebar_init_load_button = Button("LOAD", button_size="small")
    sidebar_init_load_button.disable()
    sidebar_init_input_container = Container(
        [sidebar_init_input, sidebar_init_load_button], "horizontal"
    )
    sidebar_init_input_container.hide()
    sidebar_init_input_filethumb = FileThumbnail()
    sidebar_init_input_filethumb.hide()
    sidebar_init_warning_text = Text("")
    sidebar_init_warning_text.hide()

    sidebar_init_container = Container(
        [
            sidebar_init_selector,
            sidebar_team_files_link_btn,
            sidebar_init_input_container,
            sidebar_init_input_filethumb,
            sidebar_init_warning_text,
        ]
    )
    sidebar_init_field = Field(
        sidebar_init_container,
        "Initialization",
        "Build augs pipeline from scratch or load augs from existing pipeline (safe .json format)",
    )
    # --------------------------

    # Sidebar create Aug
    sidebar_params_widget = AugsListParamsSelector(aug_utils.augs_json)
    sidebar_add_to_pipeline_button = Button("Add to Pipeline", icon="zmdi zmdi-check")
    sidebar_cancel_add_to_pipeline_button = Button(
        "Cancel", icon="zmdi zmdi-close", button_type="danger"
    )
    sidebar_aug_buttons_container = Container(
        widgets=[sidebar_add_to_pipeline_button, sidebar_cancel_add_to_pipeline_button],
        direction="horizontal",
        gap=15,
        fractions=[0, 0],
    )

    sidebar_add_container = Container(
        [
            sidebar_params_widget,
            sidebar_aug_buttons_container,
        ]
    )
    sidebar_add_container.hide()
    # --------------------------

    # Sidebar layout widgets
    sidebar_layout_pipeline = AugsList()
    sidebar_layout_add_aug_button = Button(
        "Add", icon="zmdi zmdi-playlist-plus mr5", button_size="small"
    )

    sidebar_layout_reset_aug_button = Button(
        "Reset", button_type="danger", icon="zmdi zmdi-replay mr5", button_size="small"
    )

    sidebar_layout_save_btn = create_save_btn()
    sidebar_layout_buttons_container = Container(
        widgets=[
            sidebar_layout_add_aug_button,
            sidebar_layout_reset_aug_button,
            sidebar_layout_save_btn,
        ],
        direction="horizontal",
        gap=15,
        fractions=[0, 0, 0],
    )

    pipeline_sidebar_container = Container(
        widgets=[
            sidebar_init_field,
            sidebar_layout_pipeline,
            sidebar_layout_buttons_container,
            sidebar_add_container,
        ]
    )
    # --------------------------

    return (
        # Sidebar Initialization widgets
        sidebar_init_selector,
        sidebar_team_files_link_btn,
        sidebar_init_input,
        sidebar_init_load_button,
        sidebar_init_input_container,
        sidebar_init_input_filethumb,
        sidebar_init_warning_text,
        sidebar_init_container,
        sidebar_init_field,
        # Sidebar create Aug
        sidebar_params_widget,
        sidebar_add_to_pipeline_button,
        sidebar_cancel_add_to_pipeline_button,
        sidebar_add_container,
        # Sidebar layout widgets
        sidebar_layout_pipeline,
        sidebar_layout_add_aug_button,
        sidebar_layout_reset_aug_button,
        sidebar_layout_save_btn,
        sidebar_layout_buttons_container,
        pipeline_sidebar_container,
    )

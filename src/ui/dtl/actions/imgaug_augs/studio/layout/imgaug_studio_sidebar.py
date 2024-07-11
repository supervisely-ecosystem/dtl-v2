from supervisely.app.widgets import (
    Container,
    Button,
    Field,
    Select,
    Checkbox,
    InputNumber,
    ReloadableArea,
    Input,
    FileThumbnail,
)
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
    # sidebar_init_new_button = Button("NEW", button_size="small")
    # sidebar_init_selector_container = Container(
    #     [sidebar_init_selector, sidebar_init_new_button], "horizontal"
    # )

    sidebar_init_input = Input(placeholder="Please input path to json configuration in Team Files")
    sidebar_init_input_button = Button("LOAD", button_size="small")
    sidebar_init_input_button.disable()
    sidebar_init_input_container = Container(
        [sidebar_init_input, sidebar_init_input_button], "horizontal"
    )
    sidebar_init_input_container.hide()
    sidebar_init_input_filethumb = FileThumbnail()
    sidebar_init_input_filethumb.hide()
    sidebar_init_container = Container(
        [sidebar_init_selector, sidebar_init_input_container, sidebar_init_input_filethumb]
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
        "ADD", icon="zmdi zmdi-playlist-plus mr5", button_size="small"
    )

    sidebar_layout_save_btn = create_save_btn()
    sidebar_layout_buttons_container = Container(
        widgets=[sidebar_layout_add_aug_button, sidebar_layout_save_btn],
        direction="horizontal",
        gap=15,
        fractions=[0, 0],
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
        # sidebar_init_new_button,
        # sidebar_init_selector_container,
        sidebar_init_input,
        sidebar_init_input_button,
        sidebar_init_input_container,
        sidebar_init_input_filethumb,
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
        sidebar_layout_save_btn,
        sidebar_layout_buttons_container,
        pipeline_sidebar_container,
    )

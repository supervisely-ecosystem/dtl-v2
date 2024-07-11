from supervisely.app.widgets import Container, Button
from src.ui.widgets.augs_list import AugsList
from src.ui.widgets.augs_list_params_selector import AugsListParamsSelector
from src.ui.dtl.utils import create_save_btn
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as aug_utils


def create_sidebar_widgets():
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
            sidebar_layout_pipeline,
            sidebar_layout_buttons_container,
            sidebar_add_container,
        ]
    )
    # --------------------------

    return (
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

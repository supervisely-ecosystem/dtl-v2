from src.ui.widgets.augs_list import AugsList
from supervisely.app.widgets import (
    Container,
    Button,
    Field,
    Select,
    Checkbox,
    InputNumber,
    ReloadableArea,
)
import src.ui.dtl.actions.imgaug_augs.studio.layout.utils as aug_utils


def create_sidebar_widgets():
    # Sidebar Aug category widgets
    sidebar_category_items = [Select.Item(category, category) for category in aug_utils.augs_json]
    sidebar_category_selector = Select(sidebar_category_items)
    sidebar_category_field = Field(
        sidebar_category_selector, "Augmenter Category", "Choose augmentation category"
    )
    # --------------------------

    # Sidebar Aug method widgets
    sidebar_method_list = aug_utils.augs_json.get(sidebar_category_selector.get_value())
    sidebar_method_items = [Select.Item(func, func) for func in sidebar_method_list]
    sidebar_method_selector = Select(sidebar_method_items)
    sidebar_method_field = Field(
        sidebar_method_selector, "Transformation", "Choose augmentation function"
    )
    # --------------------------

    # Sidebar Aug probability widgets
    DEFAULT_SOMETIMES_VALUE = 0.5
    sidebar_sometimes_check = Checkbox(content="probability")
    sidebar_sometimes_input = InputNumber(DEFAULT_SOMETIMES_VALUE, 0, 1, 0.01)
    sidebar_sometimes_input.disable()
    sidebar_sometimes_container = Container(
        [sidebar_sometimes_check, sidebar_sometimes_input], "horizontal"
    )
    sidebar_sometimes_field = Field(
        sidebar_sometimes_container, "Apply sometimes", "apply aug with given probability"
    )
    # --------------------------

    # Sidebar Aug params widgets
    sidebar_params_widgets = aug_utils.get_params_widget(
        sidebar_category_selector.get_value(), sidebar_method_selector.get_value()
    )

    sidebar_params_container = Container(sidebar_params_widgets)
    sidebar_params_reloadable = ReloadableArea(sidebar_params_container)
    sidebar_params_field = Field(
        sidebar_params_reloadable,
        "Params",
        "Configure current augmentation",
    )
    # --------------------------

    # Sidebar add Aug
    sidebar_add_to_pipeline_button = Button("ADD TO PIPELINE", icon="zmdi zmdi-check")
    sidebar_add_container = Container(
        [
            sidebar_category_field,
            sidebar_method_field,
            sidebar_sometimes_field,
            sidebar_params_field,
            sidebar_add_to_pipeline_button,
        ]
    )
    # --------------------------

    # Sidebar layout widgets
    sidebar_layout_pipeline = AugsList()
    sidebar_layout_add_aug_button = Button(
        "ADD", icon="zmdi zmdi-playlist-plus mr5", button_size="small"
    )
    sidebar_layout_aug_add_field = Field(
        sidebar_add_container, "Add aug to pipeline", "Explore, configure and preview"
    )
    pipeline_sidebar_container = Container(
        widgets=[
            sidebar_layout_pipeline,
            sidebar_layout_add_aug_button,
            sidebar_layout_aug_add_field,
        ]
    )
    # --------------------------

    return (
        # Sidebar Aug category widgets
        sidebar_category_items,
        sidebar_category_selector,
        sidebar_category_field,
        # Sidebar Aug method widgets
        sidebar_method_list,
        sidebar_method_items,
        sidebar_method_selector,
        sidebar_method_field,
        # Sidebar Aug probability widgets
        sidebar_sometimes_check,
        sidebar_sometimes_input,
        sidebar_sometimes_container,
        sidebar_sometimes_field,
        # Sidebar Aug params widgets
        sidebar_params_widgets,
        sidebar_params_container,
        sidebar_params_reloadable,
        sidebar_params_field,
        # Sidebar add Aug
        sidebar_add_to_pipeline_button,
        sidebar_add_container,
        # Sidebar layout widgets
        sidebar_layout_pipeline,
        sidebar_layout_add_aug_button,
        sidebar_layout_aug_add_field,
        pipeline_sidebar_container,
    )

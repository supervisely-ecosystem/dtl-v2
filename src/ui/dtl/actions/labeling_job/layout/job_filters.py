from src.ui.dtl.utils import (
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
)
from supervisely.app.widgets import (
    Button,
    Container,
    Text,
    Field,
    InputNumber,
    Checkbox,
)


def create_job_filters_widgets() -> tuple:
    # SIDEBAR SETTINGS
    # OBJECTS LIMIT PER ITEM
    lj_filters_objects_limit_per_item_widget = InputNumber(
        value=0, step=1, size="small", controls=True
    )
    lj_filters_objects_limit_per_item_widget.hide()

    lj_filters_objects_limit_checkbox = Checkbox("Unlimited", checked=True)
    lj_filters_objects_limit_container = Container(
        [lj_filters_objects_limit_checkbox, lj_filters_objects_limit_per_item_widget]
    )
    lj_filters_objects_limit_field = Field(
        title="Objects Limit Per Item",
        description="Select objects limit per item that will be available to annotators",
        content=lj_filters_objects_limit_container,
    )
    # ----------------------------

    # TAGS LIMIT PER ITEM
    lj_filters_tags_limit_per_item_widget = InputNumber(
        value=0, step=1, size="small", controls=True
    )
    lj_filters_tags_limit_per_item_widget.hide()
    lj_filters_tags_limit_checkbox = Checkbox("Unlimited", checked=True)

    lj_filters_tags_limit_container = Container(
        [lj_filters_tags_limit_checkbox, lj_filters_tags_limit_per_item_widget]
    )
    lj_filters_tags_limit_field = Field(
        title="Tags Limit Per Item",
        description="Select tags limit per item that will be available to annotators",
        content=lj_filters_tags_limit_container,
    )
    # ----------------------------

    lj_filters_save_btn = create_save_btn()
    lj_filters_sidebar_container = Container(
        [lj_filters_objects_limit_field, lj_filters_tags_limit_field, lj_filters_save_btn]
    )
    # ----------------------------

    # PREVIEW
    lj_filters_objects_limit_preview_text = Text(
        "Objects limit per item: unlimited", "text", font_size=get_text_font_size()
    )
    lj_filters_tags_limit_preview_text = Text(
        "Tags limit per item: unlimited", "text", font_size=get_text_font_size()
    )

    lj_filters_preview_container = Container(
        [
            lj_filters_objects_limit_preview_text,
            lj_filters_tags_limit_preview_text,
        ]
    )
    # ----------------------------

    # LAYOUT
    lj_filters_edit_text = Text("Filters", status="text", font_size=get_text_font_size())
    lj_filters_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    lj_filters_edit_container = get_set_settings_container(
        lj_filters_edit_text, lj_filters_edit_btn
    )
    # ----------------------------

    return (
        # sidebar
        lj_filters_objects_limit_per_item_widget,
        lj_filters_objects_limit_checkbox,
        lj_filters_tags_limit_per_item_widget,
        lj_filters_tags_limit_checkbox,
        lj_filters_sidebar_container,
        lj_filters_save_btn,
        # preview
        lj_filters_objects_limit_preview_text,
        lj_filters_tags_limit_preview_text,
        lj_filters_preview_container,
        # layout
        lj_filters_edit_container,
    )

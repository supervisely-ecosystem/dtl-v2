import src.globals as g
from src.ui.dtl.utils import (
    create_save_btn,
    get_text_font_size,
    get_set_settings_button_style,
    get_set_settings_container,
)
from src.ui.widgets import TagsListPreview
from supervisely.app.widgets import Button, Container, Text, TagsTable, Field


def create_tags_selector_widgets():
    # Sidebar
    src_tags_widget = TagsTable()
    src_tags_save_btn = create_save_btn()
    src_tags_set_default_btn = Button(
        "Set Default", button_type="info", plain=True, icon="zmdi zmdi-refresh"
    )

    src_tags_field = Field(
        content=src_tags_widget,
        title="Tags",
        description=(
            "Select tags that will be used in data transformation processes. "
            "If tag is not selected, it will be ignored."
        ),
    )
    src_tags_widgets_container = Container(
        widgets=[
            src_tags_field,
            Container(
                widgets=[
                    src_tags_save_btn,
                    src_tags_set_default_btn,
                ],
                direction="horizontal",
                gap=0,
                fractions=[1, 0],
                # gap=355,
            ),
        ]
    )

    # Preview
    src_tags_preview = TagsListPreview()
    # Layout
    src_tags_edit_text = Text("Tags", status="text", font_size=get_text_font_size())
    src_tags_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )

    if g.PROJECT_ID is None:
        src_tags_edit_btn.disable()

    src_tags_edit_contaniner = get_set_settings_container(src_tags_edit_text, src_tags_edit_btn)

    return (
        # Sidebar
        src_tags_widget,
        src_tags_save_btn,
        src_tags_set_default_btn,
        src_tags_field,
        src_tags_widgets_container,
        # Preview
        src_tags_preview,
        # Layout
        src_tags_edit_text,
        src_tags_edit_btn,
        src_tags_edit_contaniner,
    )

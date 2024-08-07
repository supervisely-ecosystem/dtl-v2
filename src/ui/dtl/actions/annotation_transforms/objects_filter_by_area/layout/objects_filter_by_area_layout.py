from supervisely.app.widgets import Container, Button, Text
from src.ui.dtl.utils import (
    get_text_font_size,
    get_set_settings_container,
    get_set_settings_button_style,
    get_text_font_size,
)
from supervisely.app.widgets import Container, Button, Text
from src.ui.widgets import ClassesListPreview, TagsListPreview


def create_layout_widgets():
    # Layout
    layout_edit_text = Text("Settings", status="text", font_size=get_text_font_size())
    layout_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    layout_edit_container = get_set_settings_container(layout_edit_text, layout_edit_btn)
    # --------------------------------

    # Preview
    layout_classes_preview_text = Text(
        "Classes: 0 / 0", status="text", font_size=get_text_font_size()
    )
    layout_classes_preview = ClassesListPreview()

    layout_classes_preview_container = Container(
        widgets=[layout_classes_preview_text, layout_classes_preview], gap=1
    )

    layout_preview_area = Text("Area size:", status="text", font_size=get_text_font_size())
    layout_preview_condition = Text("Condition:", status="text", font_size=get_text_font_size())
    layout_preview_action = Text("Action:", status="text", font_size=get_text_font_size())
    layout_tags_preview_text = Text("Tags: 0 / 0", status="text", font_size=get_text_font_size())
    layout_preview_tags = TagsListPreview()
    layout_preview_container = Container(
        widgets=[
            layout_preview_area,
            layout_preview_condition,
            layout_preview_action,
            layout_tags_preview_text,
            layout_preview_tags,
        ],
        gap=1,
    )

    # Hide preview widgets until selected
    layout_preview_area.hide()
    layout_preview_condition.hide()
    layout_preview_action.hide()
    layout_tags_preview_text.hide()
    layout_preview_tags.hide()
    # layout_preview_container.hide()

    return (
        # Layout
        layout_edit_text,
        layout_edit_btn,
        layout_edit_container,
        # Preview
        layout_classes_preview_text,
        layout_classes_preview,
        layout_classes_preview_container,
        layout_preview_area,
        layout_preview_action,
        layout_preview_condition,
        layout_tags_preview_text,
        layout_preview_tags,
        layout_preview_container,
    )

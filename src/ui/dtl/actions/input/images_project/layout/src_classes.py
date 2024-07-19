import src.globals as g
from src.ui.dtl.utils import (
    create_save_btn,
    get_text_font_size,
    get_set_settings_button_style,
    get_set_settings_container,
)
from src.ui.widgets import ClassesListPreview
from supervisely.app.widgets import Button, Container, Text, ClassesTable, Field


def create_classes_selector_widgets():
    # Sidebar
    src_classes_widget = ClassesTable()
    src_classes_save_btn = create_save_btn()
    src_classes_set_default_btn = Button(
        "Set Default", button_type="info", plain=True, icon="zmdi zmdi-refresh"
    )
    src_classes_field = Field(
        content=src_classes_widget,
        title="Classes",
        description=(
            "Select classes that will be used in data transformation processes. "
            "If class is not selected, it will be ignored."
        ),
    )
    src_classes_widgets_container = Container(
        widgets=[
            src_classes_field,
            Container(
                widgets=[
                    src_classes_save_btn,
                    src_classes_set_default_btn,
                ],
                direction="horizontal",
                gap=0,
                fractions=[1, 0],
                # gap=355,
            ),
        ]
    )
    # Preview
    src_classes_preview = ClassesListPreview()

    # Layout
    src_classes_edit_text = Text("Classes", status="text", font_size=get_text_font_size())
    src_classes_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )

    if g.PROJECT_ID is None:
        src_classes_edit_btn.disable()

    src_classes_edit_contaniner = get_set_settings_container(
        src_classes_edit_text, src_classes_edit_btn
    )

    return (
        # Sidebar
        src_classes_widget,
        src_classes_save_btn,
        src_classes_set_default_btn,
        src_classes_field,
        src_classes_widgets_container,
        # Preview
        src_classes_preview,
        # Layout
        src_classes_edit_text,
        src_classes_edit_btn,
        src_classes_edit_contaniner,
    )

from supervisely.app.widgets import (
    Container,
    Button,
    Text,
)
from src.ui.dtl.utils import (
    get_text_font_size,
    get_set_settings_button_style,
    get_text_font_size,
)


def create_layout_widgets():
    # Layout
    layout_text = Text("Select split method", status="text", font_size=get_text_font_size())
    layout_edit_button = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    layout_container = Container(
        widgets=[layout_text, layout_edit_button],
        direction="horizontal",
        style="place-items: center",
    )
    # --------------------------

    # Preview
    layout_current_method = Text(
        "Current method: None", status="text", font_size=get_text_font_size()
    )
    # --------------------------

    return (
        # Layout
        layout_text,
        layout_edit_button,
        layout_container,
        # Preview
        layout_current_method,
    )

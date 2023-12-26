from supervisely.app.widgets import (
    Text,
    Button,
)

from src.ui.dtl.utils import (
    get_set_settings_button_style,
    get_set_settings_container,
)


def create_model_serve_widgets():
    model_serve_preview = Text(font_size=13)
    model_serve_btn = Button(
        text="SERVE",
        icon="zmdi zmdi-play",
        button_type="text",
        button_size="small",
        style=get_set_settings_button_style(),
    )
    model_serve_layout_container = get_set_settings_container(model_serve_preview, model_serve_btn)
    return model_serve_preview, model_serve_btn, model_serve_layout_container

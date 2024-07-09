from supervisely.app.widgets import (
    Container,
    Button,
    Text,
)
from src.ui.widgets.augs_list_preview import AugsListPreview
from src.ui.dtl.utils import (
    get_text_font_size,
    get_set_settings_button_style,
    get_text_font_size,
)


def create_layout_widgets():
    # Layout
    layout_text = Text("Edit Augmentation Pipeline", status="text", font_size=get_text_font_size())
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
    layout_pipeline_preview = AugsListPreview(
        pipeline=[],
        max_height="128px",
        empty_text="No augmentations",
    )
    layout_shuffle_preview = Text(
        "Randomize order: False", status="text", font_size=get_text_font_size()
    )
    layout_preview_container = Container([layout_pipeline_preview, layout_shuffle_preview])
    # --------------------------

    return (
        # Layout
        layout_text,
        layout_edit_button,
        layout_container,
        # Preview
        layout_pipeline_preview,
        layout_shuffle_preview,
        layout_preview_container,
    )

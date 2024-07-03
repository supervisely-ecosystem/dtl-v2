from supervisely.app.widgets import NodesFlow, Container, Button, Text, Field
import src.globals as g


def get_set_settings_button_style():
    return "flex: auto; border: 1px solid #bfcbd9; color: black; background-color: white;"


def get_text_font_size():
    return 13


def create_pipeline_widgets():
    ### LAYOUT
    pipeline_layout_text = Text("Select agent", status="text", font_size=get_text_font_size())
    pipeline_layout_edit_button = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    pipeline_layout_container = Container(
        widgets=[pipeline_layout_text, pipeline_layout_edit_button],
        direction="horizontal",
        style="place-items: center",
    )

    ### SIDEBAR

    # pipeline widget
    pipeline_widget = 123

    # actions
    add_button = Button("ADD", icon="zmdi zmdi-playlist-plus mr5", button_size="small")
    preview_button = Button("PREVIEW", icon="zmdi zmdi-slideshow mr5", button_size="small")
    export_button = Button("EXPORT", icon="zmdi zmdi-floppy mr5", button_size="small")

    actions_container = Container(
        widgets=[add_button, preview_button, export_button], direction="horizontal"
    )
    pipeline_sidebar_container = Container(widgets=[pipeline_widget, actions_container])

    pipeline_sidebar_field = Field(
        pipeline_sidebar_container,
        title="Your custom augmentation pipeline",
        description="Add transformations in a sequence, preview the results of individual aug or a whole pipeline",
    )

    return (
        pipeline_layout_text,
        pipeline_layout_edit_button,
        pipeline_layout_container,
        pipeline_widget,
        add_button,
        preview_button,
        export_button,
        actions_container,
        pipeline_sidebar_container,
        pipeline_sidebar_field,
    )

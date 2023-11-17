from supervisely.app.widgets import (
    Button,
    Container,
    Flexbox,
    Text,
    Field,
    Editor,
    Select,
    Input,
    Checkbox,
)
from src.ui.dtl.utils import (
    get_set_settings_button_style,
    get_set_settings_container,
    create_save_btn,
    create_set_default_btn,
    get_text_font_size,
)

### SIDEBAR LAYOUT
suffix_input = Input(value="model", size="small")
suffix_field = Field(
    title="Class / Tag name suffix",
    description="Add suffix to model class / tag name, if it has conflicts with existing one",
    content=suffix_input,
)

always_add_suffix_checkbox = Checkbox(
    content=Text("<b>Always add suffix to model predictions</b>", "text")
)


resolve_conflict_methods = [
    Select.Item(value="merge", label="Merge"),
    Select.Item(value="replace", label="Replace"),
]
resolve_conflict_method_selector = Select(resolve_conflict_methods, size="small")
resolve_conflict_method_field = Field(
    title="Resolve conflict method",
    description="Select how to resolve conflict between model classes / tags and existing ones",
    content=resolve_conflict_method_selector,
)

inf_settings_editor = Editor(
    initial_text="Connect to model first",
    language_mode="yaml",
    restore_default_button=False,
    readonly=True,
)
inf_settings_editor_field = Field(
    title="Settings",
    description="Model specific inference settings in YAML format",
    content=inf_settings_editor,
)

inf_settings_save_btn = create_save_btn()
inf_settings_set_default_btn = create_set_default_btn()

inf_settings_widgets_container = Container(
    widgets=[
        suffix_field,
        always_add_suffix_checkbox,
        resolve_conflict_method_field,
        inf_settings_editor_field,
        Flexbox(
            widgets=[
                inf_settings_save_btn,
                inf_settings_set_default_btn,
            ],
            gap=110,
        ),
    ]
)
### ------------------------------------------------------

### NODE LAYOUT
inf_settings_edit_text = Text("Inference Settings", "text", font_size=get_text_font_size())
inf_settings_edit_btn = Button(
    text="EDIT",
    icon="zmdi zmdi-edit",
    button_type="text",
    button_size="small",
    emit_on_click="openSidebar",
    style=get_set_settings_button_style(),
)
inf_settings_edit_container = get_set_settings_container(
    inf_settings_edit_text, inf_settings_edit_btn
)

# @TODO: add settings preview

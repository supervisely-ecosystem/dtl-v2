from supervisely.app.widgets import (
    Text,
    Button,
    Container,
    RadioTabs,
    CustomModelsSelector,
    PretrainedModelsSelector,
    Checkbox,
    Select,
)


import src.globals as g
from src.ui.dtl.utils import (
    get_text_font_size,
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
)


def create_model_selector_widgets(
    framework_name: str, pretrained_models: list, custom_models: list, custom_task_types: list = []
):
    # SIDEBAR

    # CUSTOM MODEL OPTION SUPERVISELY
    need_custom_task_types = len(custom_task_types) > 0

    model_selector_sidebar_custom_model_table = CustomModelsSelector(
        g.TEAM_ID,
        custom_models,
        need_custom_task_types,
        custom_task_types,
    )

    custom_models_task_types = model_selector_sidebar_custom_model_table.get_available_task_types()
    if "object detection" in custom_models_task_types:
        model_selector_sidebar_custom_model_table.set_active_task_type("object detection")
    # ------------------------------

    # PUBLIC MODEL OPTIONS
    model_selector_sidebar_public_model_table = PretrainedModelsSelector(pretrained_models)
    pretrained_model_selector_task_types = (
        model_selector_sidebar_public_model_table.get_available_task_types()
    )
    if "object detection" in pretrained_model_selector_task_types:
        model_selector_sidebar_public_model_table.set_active_task_type("object detection")
    available_runtimes = ["PyTorch", "ONNXRuntime", "TensorRT"]
    model_selector_runtime_selector_sidebar = Select(
        [Select.Item(runtime, runtime) for runtime in available_runtimes]
    )
    model_selector_sidebar_public_container = Container(
        [model_selector_sidebar_public_model_table, model_selector_runtime_selector_sidebar]
    )
    # ------------------------------

    # CUSTOM /PUBLIC TABS
    model_selector_sidebar_model_source_tabs = RadioTabs(
        titles=["Custom models", "Pretrained public models"],
        descriptions=["Models trained by you", f"Models trained by {framework_name} team"],
        contents=[
            model_selector_sidebar_custom_model_table,
            model_selector_sidebar_public_container,
        ],
    )
    if len(custom_models) == 0:
        model_selector_sidebar_model_source_tabs.set_active_tab("Pretrained public models")

    # SIDEBAR CONTAINER
    model_selector_sidebar_save_btn = create_save_btn()
    model_selector_sidebar_container = Container(
        [
            model_selector_sidebar_model_source_tabs,
            model_selector_sidebar_save_btn,
        ]
    )
    # ------------------------------

    # PREVIEW
    # TODO: App thumbnail widget
    model_selector_preview = Text("Checkpoint:", status="text", font_size=get_text_font_size())
    model_selector_preview.hide()
    model_selector_preview_type = Text("Type:", status="text", font_size=get_text_font_size())
    model_selector_preview_type.hide()
    # ------------------------------

    # LAYOUT
    # STOP MODEL AFTER INFERENCE
    model_selector_stop_model_after_pipeline_checkbox = Checkbox(
        Text("Auto stop model on pipeline finish", "text", font_size=13), True
    )

    model_selector_layout_edit_text = Text(
        "Select model", status="text", font_size=get_text_font_size()
    )
    model_selector_layout_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )

    model_selector_layout_container = get_set_settings_container(
        model_selector_layout_edit_text, model_selector_layout_edit_btn
    )
    # ------------------------------

    return (
        # sidebar
        # custom options
        model_selector_sidebar_custom_model_table,
        # public options
        model_selector_sidebar_public_model_table,
        model_selector_runtime_selector_sidebar,
        model_selector_sidebar_public_container,
        # sidebar
        model_selector_sidebar_model_source_tabs,
        model_selector_sidebar_save_btn,
        model_selector_sidebar_container,
        # preview
        model_selector_preview,
        model_selector_preview_type,
        # layout
        model_selector_layout_edit_text,
        model_selector_layout_edit_btn,
        model_selector_layout_container,
        model_selector_stop_model_after_pipeline_checkbox,
    )

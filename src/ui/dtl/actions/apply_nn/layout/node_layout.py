from supervisely.app.widgets import NodesFlow

from src.ui.dtl.actions.apply_nn.layout.connect_model import *
from src.ui.dtl.actions.apply_nn.layout.select_classes import *
from src.ui.dtl.actions.apply_nn.layout.select_tags import *
from src.ui.dtl.actions.apply_nn.layout.apply_method import *
from src.ui.dtl.actions.apply_nn.layout.inference_settings import *

### UPDATE PREVIEW BUTTON
update_preview_btn = Button(
    text="Update",
    icon="zmdi zmdi-refresh",
    button_type="text",
    button_size="small",
    style=get_set_settings_button_style(),
)
update_preview_btn.disable()
### -----------------------------


def create_layout():
    settings_options = [
        NodesFlow.Node.Option(
            name="Connect to Model",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=connect_nn_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(connect_nn_widgets_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            "model_preview",
            option_component=NodesFlow.WidgetOptionComponent(connect_nn_model_preview),
        ),
        NodesFlow.Node.Option(
            name="Select Classes",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=classes_list_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(classes_list_widgets_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            "classes_preview",
            option_component=NodesFlow.WidgetOptionComponent(classes_list_preview),
        ),
        NodesFlow.Node.Option(
            name="Select Tags",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=tags_list_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(tags_list_widgets_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            "tags_preview",
            option_component=NodesFlow.WidgetOptionComponent(tags_list_preview),
        ),
        NodesFlow.Node.Option(
            name="Inference Settings",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=inf_settings_edit_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(inf_settings_widgets_container),
                sidebar_width=380,
            ),
        ),
        NodesFlow.Node.Option(
            "anonymize_type",
            option_component=NodesFlow.WidgetOptionComponent(apply_nn_method_container),
        ),
    ]
    return settings_options

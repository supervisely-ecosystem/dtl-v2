import time
from supervisely.app.widgets import (
    Select,
    Container,
    Button,
    Flexbox,
    Dialog,
    NodesFlow,
    Field,
    Text,
    Empty,
    Sidebar,
    Input,
    Draggable,
)
from supervisely.app import show_dialog
from supervisely import ProjectMeta

from src.ui.dtl.Layer import Layer
from src.ui.dtl import actions, actions_list
from src.ui.dtl import SOURCE_ACTIONS
import src.utils as utils
import src.ui.utils as ui_utils
from src.exceptions import CustomException
from src.exceptions import handle_exception
import src.globals as g
from src.compute.Net import Net


# context menu "select" option dialog
select_action_name = Select(
    groups=[
        Select.Group(
            group_name,
            items=[
                Select.Item(action_name, actions[action_name].title)
                for action_name in group_actions
            ],
        )
        for group_name, group_actions in actions_list.items()
    ],
    filterable=True,
    size="large",
)
add_layer_from_dialog_btn = Button("Add Layer")
add_layer_dialog = Dialog(
    title="Add Layer",
    content=Flexbox(widgets=[select_action_name, add_layer_from_dialog_btn]),
    size="tiny",
)

# context / drag and drop menu items
context_menu_items = [
    {"label": "Select...", "key": "__select__"},
    *[
        {
            "label": group_name,
            "items": [
                {"key": action_name, "label": actions[action_name].title}
                for action_name in group_actions
            ],
            "divided": group_name == SOURCE_ACTIONS,
        }
        for group_name, group_actions in actions_list.items()
    ],
    {"label": "Clear", "key": "__clear__", "divided": True},
]

nodes_flow = NodesFlow(
    height="calc(100vh - 195px)",
    context_menu=context_menu_items,
    color_theme="white",
    show_save=False,
)


# sidebar
add_specific_layer_buttons = {
    action_name: Button(
        "Add", icon="zmdi zmdi-plus", style="align-self: start;", button_size="small"
    )
    for _, group_actions in actions_list.items()
    for action_name in group_actions
}


def add_specific_layer_func_factory(action_name: str):
    def add_specific_layer_func():
        add_layer(action_name)

    return add_specific_layer_func


for action_name, button in add_specific_layer_buttons.items():
    button.click(add_specific_layer_func_factory(action_name))

filter_actions_input = Input(placeholder="Filter...")
filter_actions_field = Field(content=filter_actions_input, title="Filter actions")

left_sidebar_actions_widgets = {
    action_name: Draggable(
        Flexbox(
            widgets=[
                Field(
                    title=action.title,
                    description=action.description,
                    title_url=action.docs_url,
                    content=Empty(),
                ),
                add_specific_layer_buttons[action_name],
            ]
        ),
        key=action_name,
    )
    for action_name, action in actions.items()
}

left_sidebar_groups_widgets = {
    group_name: Container(
        widgets=[
            Text(f"<h3>{group_name}</h3>"),
            Container(
                widgets=[
                    left_sidebar_actions_widgets[action_name] for action_name in group_actions
                ],
                gap=0,
            ),
        ]
    )
    for group_name, group_actions in actions_list.items()
}


left_sidebar_widgets = [
    filter_actions_field,
    *[left_sidebar_groups_widgets[group_name] for group_name in actions_list.keys()],
]
sidebar = Sidebar(
    left_content=Container(widgets=left_sidebar_widgets, style="padding-top: 10px;"),
    right_content=nodes_flow,
    width_percent=20,
    standalone=False,
    height="calc(100vh - 195px)",
)

layout = Container(widgets=[add_layer_dialog, sidebar])


@handle_exception
def add_layer(action_name: str, position: dict = None):
    try:
        layer = ui_utils.create_new_layer(action_name)
        node = ui_utils.create_node(layer, position)
        nodes_flow.add_node(node)
    except CustomException as e:
        ui_utils.show_error("Error adding layer", e)
        raise
    except Exception as e:
        show_dialog(
            title="Error adding layer", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise


@nodes_flow.context_menu_clicked
def context_menu_clicked_cb(item):
    position = item["position"]
    g.context_menu_position = position
    action_name = item["item"]["key"]
    if action_name == "__select__":
        add_layer_dialog.show()
        return
    if action_name == "__clear__":
        nodes_flow.clear()
        return
    add_layer(action_name, position)
    g.context_menu_position = None


@nodes_flow.item_dropped
def item_dropped_cb(item):
    print(item)
    position = item["position"]
    g.context_menu_position = position
    action_name = item["item"]["key"]
    add_layer(action_name, position)
    g.context_menu_position = None


@add_layer_from_dialog_btn.click
def add_layer_from_dialog_btn_cb():
    position = g.context_menu_position
    action_name = select_action_name.get_value()
    add_layer(action_name, position)
    add_layer_dialog.hide()
    g.context_menu_position = None


@filter_actions_input.value_changed
def filter(value):
    g.cache["last_search"] = value
    time.sleep(0.4)
    if g.cache["last_search"] != value:
        return

    if value == "":
        for group_name, group_actions in actions_list.items():
            for action_name in group_actions:
                left_sidebar_actions_widgets[action_name].show()
            left_sidebar_groups_widgets[group_name].show()
    else:
        value = value.lower()
        for group_name, group_actions in actions_list.items():
            found = False
            for action_name in group_actions:
                if (
                    action_name.lower().find(value) == -1
                    and actions[action_name].title.lower().find(value) == -1
                ):
                    left_sidebar_actions_widgets[action_name].hide()
                else:
                    left_sidebar_actions_widgets[action_name].show()
                    found = True
            if found:
                left_sidebar_groups_widgets[group_name].show()
            else:
                left_sidebar_groups_widgets[group_name].hide()


@handle_exception
def update_nodes():
    try:
        for layer in g.layers.values():
            layer.set_preview_loading(True)

        edges = nodes_flow.get_edges_json()
        nodes_state = nodes_flow.get_nodes_state_json()

        # Init layers data
        layers_ids = ui_utils.init_layers(nodes_state)
        data_layers_ids = layers_ids["data_layers_ids"]
        all_layers_ids = layers_ids["all_layers_ids"]

        # Call meta changed callbacks for Data layers
        for layer_id in data_layers_ids:
            layer = g.layers[layer_id]
            layer: Layer
            src = layer.get_src()
            layer_input_meta = ProjectMeta()
            if src:
                project_name, _ = src[0].split("/")
                layer_input_meta = utils.get_project_meta(
                    utils.get_project_by_name(project_name).id
                )
            layer.update_project_meta(layer_input_meta)

        # Init sources
        ui_utils.init_src(edges)

        # Calculate output metas for all layers
        utils.delete_results_dir()
        utils.create_results_dir()
        dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
        net = Net(dtl_json, g.RESULTS_DIR)
        net.preview_mode = True
        net = ui_utils.init_output_metas(net, all_layers_ids, nodes_state, edges)

        # Load preview for data layers
        utils.delete_preview_dir()
        utils.create_preview_dir()
        ui_utils.set_preview(data_layers_ids)

        # Update preview
        ui_utils.update_previews(net, data_layers_ids, all_layers_ids)

    except CustomException as e:
        ui_utils.show_error("Error updating nodes", e)
        raise e
    except Exception as e:
        show_dialog(
            title="Error updating nodes", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise e
    finally:
        for layer in g.layers.values():
            layer.set_preview_loading(False)


@handle_exception
def update_metas():
    try:
        edges = nodes_flow.get_edges_json()
        nodes_state = nodes_flow.get_nodes_state_json()

        # Init layers data
        layers_ids = ui_utils.init_layers(nodes_state)
        all_layers_ids = layers_ids["all_layers_ids"]
        data_layers_ids = layers_ids["data_layers_ids"]

        # Call meta changed callbacks for Data layers
        for layer_id in data_layers_ids:
            layer = g.layers[layer_id]
            layer: Layer
            src = layer.get_src()
            layer_input_meta = ProjectMeta()
            if src:
                project_name, _ = src[0].split("/")
                layer_input_meta = utils.get_project_meta(
                    utils.get_project_by_name(project_name).id
                )
            layer.update_project_meta(layer_input_meta)

        # Init sources
        ui_utils.init_src(edges)

        # Calculate output metas for all layers
        utils.delete_results_dir()
        utils.create_results_dir
        dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
        net = Net(dtl_json, g.RESULTS_DIR)
        net.preview_mode = True
        ui_utils.init_output_metas(net, all_layers_ids, nodes_state, edges)

    except CustomException as e:
        ui_utils.show_error("Error updating nodes", e)
        raise e
    except Exception as e:
        show_dialog(
            title="Error updating nodes", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise e


def update_nodes_cb():
    g.updater("nodes")


def update_metas_cb():
    g.updater("metas")


@nodes_flow.sidebar_toggled
def sidebar_toggled_cb():
    print("sidebar toggled")


nodes_flow.flow_changed(update_metas_cb)
nodes_flow.flow_state_changed(update_metas_cb)
nodes_flow.on_save(update_metas_cb)

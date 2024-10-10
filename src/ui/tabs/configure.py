import random
import time
import threading
from collections import defaultdict
from typing import List

# import random
from supervisely.app.widgets import (
    Select,
    Container,
    Button,
    Flexbox,
    Dialog,
    NodesFlow,
    Field,
    Text,
    Sidebar,
    Input,
    Markdown,
    OneOf,
    Card,
)
from supervisely.app import show_dialog
from supervisely.sly_logger import logger
from src.ui.dtl.Action import ApplyNNAction, DeployNNAction, SourceAction

from src.ui.dtl.Layer import Layer
from src.ui.dtl import actions_dict, actions_list
from src.ui.dtl import SOURCE_ACTIONS
import src.utils as utils
import src.ui.utils as ui_utils
from src.exceptions import CustomException
from src.exceptions import handle_exception
import src.globals as g
from src.compute.Net import Net
from src.ui.widgets import LayerCard

from supervisely.app.content import StateJson


nodes_flow_lock = threading.Lock()

# context menu "select" option dialog
select_action_name = Select(
    groups=[
        Select.Group(
            group_name,
            items=[
                Select.Item(action_name, actions_dict[action_name].title)
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
                {"key": action_name, "label": actions_dict[action_name].title}
                for action_name in group_actions
            ],
            "divided": group_name == SOURCE_ACTIONS,
        }
        for group_name, group_actions in actions_list.items()
    ],
    {"label": "Clear", "key": "__clear__", "divided": True},
]


class CustomNodesFlow(NodesFlow):
    def replace_node(self, node_idx, node: NodesFlow.Node):
        self._nodes[node_idx] = node
        StateJson()[self.widget_id]["flow"]["nodes"][node_idx] = node.to_json()
        StateJson().send_changes()

    def add_node(self, node: NodesFlow.Node):
        self._nodes.append(node)
        StateJson()[self.widget_id]["flow"]["nodes"].append(node.to_json())
        len_nodes = len(StateJson()[self.widget_id]["flow"]["nodes"])
        StateJson().send_changes()
        return len_nodes - 1


nodes_flow = CustomNodesFlow(
    height="calc(100vh - 58px)",
    context_menu=context_menu_items,
    color_theme="light",
    show_save=False,
)

nodes_flow_card = Card(
    content=nodes_flow,
    lock_message="Pipeline is in progress...",
    remove_padding=True,
)

select_items = [
    Select.Item(
        value=action_name,
        label=action_name,
        content=Markdown(action.md_description, show_border=False),
    )
    for action_name, action in actions_dict.items()
]
select_widget = Select(items=select_items)
oneof_widget = OneOf(conditional_widget=select_widget)
dialog_widgets = Dialog(title="Node Documentation", content=oneof_widget)

add_specific_layer_buttons = {
    action_name: LayerCard(
        name=action.title,
        key=action_name,
        icon=action.icon,
        dialog_widget=dialog_widgets,
        selector_widget=select_widget,
        color=action.node_color,
    )
    for action_name, action in actions_dict.items()
}


def add_specific_layer_func_factory(action_name: str):
    def add_specific_layer_func():
        add_layer(action_name, autoconnect=g.connect_node_checkbox.is_checked())

    return add_specific_layer_func


for action_name, layer_card in add_specific_layer_buttons.items():
    layer_card.on_add_button(add_specific_layer_func_factory(action_name))

filter_actions_input = Input(placeholder="Start typing layer name...", icon="search")
collapse_sidebar_btn = Button(
    "",
    icon="zmdi zmdi-chevron-left",
    button_size="small",
    plain=True,
    show_loading=False,
    style="padding: 9px 11px 9px 14px",
)
left_sidebar_actions_widgets = {
    action_name: add_specific_layer_buttons[action_name]
    for action_name, action in actions_dict.items()
}

left_sidebar_groups_widgets = {
    group_name: Container(
        widgets=[
            Text(f"<b>{group_name}</b>"),
            Container(
                widgets=[
                    left_sidebar_actions_widgets[action_name] for action_name in group_actions
                ],
                gap=0,
            ),
        ],
        gap=2,
    )
    for group_name, group_actions in actions_list.items()
}

modality_type_text = Text(
    f"The list of ML Pipelines (operations) below is for <b>{g.MODALITY_TYPE}</b> modality. "
    "Run the app with different option to change the data type.",
    status="text",
    font_size=12,
)

left_sidebar_widgets = [
    Flexbox(widgets=[collapse_sidebar_btn, filter_actions_input]),
    modality_type_text,
    *[left_sidebar_groups_widgets[group_name] for group_name in actions_list.keys()],
]

sidebar = Sidebar(
    left_content=Container(widgets=left_sidebar_widgets, style="padding-top: 10px;", gap=15),
    right_content=nodes_flow_card,
    width_percent=26.1,
    standalone=True,
    height="calc(100vh - 57px)",
    clear_main_panel_paddings=True,
    show_close=False,
    sidebar_left_padding="20px",
)

layout = Container(widgets=[dialog_widgets, add_layer_dialog, sidebar], gap=0)


@collapse_sidebar_btn.click
def collapse_sidebar():
    sidebar.collapse()


def maybe_add_edges(layer: Layer):
    layer_inputs = layer.action.create_inputs()
    if not layer_inputs:
        return

    # Need this because remove_nodes is not always triggered
    nodes_json = nodes_flow.get_nodes_json()
    existing_layers = {node["id"] for node in nodes_json}
    edges = nodes_flow.get_edges_json()

    # layer input name.
    # If layer has source input, it will be "source", otherwise it will be first one
    layer_interface = layer_inputs[0].name
    for i, input_ in enumerate(layer_inputs):
        if input_.name == "source":
            layer_interface = input_.name

    src_layer_id = None
    for l_id in g.nodes_history[::-1]:
        if l_id != layer.id and l_id in existing_layers:
            last_layer: Layer = g.layers[l_id]
            outputs = last_layer.action.create_outputs()
            if outputs:
                src_layer_id = l_id
                src_layer_interface = last_layer.get_destination_name(0)

                # case with apply -> deploy
                if issubclass(last_layer.action, DeployNNAction):
                    # if last layer was deploy and current not apply, skip
                    if not issubclass(layer.action, ApplyNNAction):
                        continue
                    # if last layer was deploy and current is apply, connect to deploy input
                    for i, input_ in enumerate(layer_inputs):
                        if input_.name == "deployed_model":
                            layer_interface = input_.name
                            break
                break

    if src_layer_id is None:
        return

    edges.append(
        {
            "id": random.randint(10000000000000, 99999999999999),
            "output": {
                "node": src_layer_id,
                "interface": src_layer_interface,
            },
            "input": {
                "node": layer.id,
                "interface": layer_interface,
            },
        }
    )

    nodes_flow.set_edges(edges)
    return


# @ui_utils.debounce(0.1)
@handle_exception
def add_layer(action_name: str, position: dict = None, autoconnect: bool = False):
    with nodes_flow_lock:
        g.stop_updates = True
        try:
            layer = ui_utils.create_new_layer(action_name)
            node = ui_utils.create_node(layer, position)

            node_idx = nodes_flow.add_node(node)

            if autoconnect:
                maybe_add_edges(layer)
            if layer.init_widgets():
                nodes_json = nodes_flow.get_nodes_json()
                logger.debug(
                    "nodes_json", extra={"nodes_json len": len(nodes_json), "node_idx": node_idx}
                )
                try:
                    position = nodes_json[node_idx].get("position", None)
                except:
                    position = None
                    # raise IndexError("Node is not found in nodes_json")

                node = ui_utils.create_node(layer, position)
                # nodes_flow.replace_node(node_idx, node)
                nodes_flow.pop_node(node_idx)
                nodes_flow.add_node(node)
                if autoconnect:
                    maybe_add_edges(layer)
            g.stop_updates = False
            logger.info(f"Layer with ID: '{layer.id}' have been added")
            # g.updater(("nodes", layer.id))
        except CustomException as e:
            ui_utils.show_error("Error adding layer", e)
            raise
        except Exception as e:
            show_dialog(
                title="Error adding layer",
                description=f"Unexpected Error: {str(e)}",
                status="error",
            )
            raise
        finally:
            g.stop_updates = False
            g.updater("metas")


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
    time.sleep(0.2)
    add_layer(action_name, position, autoconnect=g.connect_node_checkbox.is_checked())
    g.context_menu_position = None


@nodes_flow.item_dropped
def item_dropped_cb(item):
    position = item["position"]
    g.context_menu_position = position
    action_name = item["item"]["key"]
    time.sleep(0.2)
    add_layer(action_name, position, autoconnect=g.connect_node_checkbox.is_checked())
    g.context_menu_position = None


@nodes_flow.node_removed
def node_removed(layer_id: str):
    if layer_id.startswith("filtered_project"):
        g.FILTERED_ENTITIES = []
        return
    if layer_id.startswith("deploy"):
        utils.kill_deployed_app_by_layer_id(layer_id)

    g.layers.pop(layer_id, None)
    if layer_id.startswith("images_project"):
        utils.clean_current_srcs()
    logger.debug("node_removed", extra={"layer_id": layer_id, "g.layers": list(g.layers.keys())})
    logger.info(f"Layer with ID: '{layer_id}' have been removed")


@add_layer_from_dialog_btn.click
def add_layer_from_dialog_btn_cb():
    position = g.context_menu_position
    action_name = select_action_name.get_value()
    time.sleep(0.2)
    add_layer(action_name, position, autoconnect=g.connect_node_checkbox.is_checked())
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
                    and actions_dict[action_name].title.lower().find(value) == -1
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
def update_nodes(layer_id: str = None):
    try:
        if layer_id is None:
            for layer in g.layers.values():
                layer.set_preview_loading(True)

            edges = nodes_flow.get_edges_json()
            nodes_state = nodes_flow.get_nodes_state_json()

            # Init layers data
            layers_ids = ui_utils.init_layers(nodes_state)
            data_layers_ids = layers_ids["data_layers_ids"]
            all_layers_ids = layers_ids["all_layers_ids"]

            # Init sources
            ui_utils.init_src(edges)

            utils.delete_results_dir()
            utils.create_results_dir()
            dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
            net = Net(dtl_json, g.RESULTS_DIR, g.MODALITY_TYPE)
            net.preview_mode = True

            # Load preview for data layers
            utils.delete_preview_dir()
            utils.create_preview_dir()

            # Update preview
            ui_utils.update_all_previews(net, data_layers_ids, all_layers_ids)

        else:
            layer = g.layers[layer_id]
            layer: Layer
            layer.set_preview_loading(True)

            edges = nodes_flow.get_edges_json()
            nodes_state = nodes_flow.get_nodes_state_json()

            # Init layers data
            layers_ids = ui_utils.init_layers(nodes_state)
            data_layers_ids = layers_ids["data_layers_ids"]
            all_layers_ids = layers_ids["all_layers_ids"]

            # Init sources
            ui_utils.init_src(edges)

            utils.delete_results_dir()
            utils.create_results_dir()
            dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
            net = Net(dtl_json, g.RESULTS_DIR, g.MODALITY_TYPE)
            net.preview_mode = True

            ui_utils.init_nodes_state(net, data_layers_ids, all_layers_ids, nodes_state, edges)
            ui_utils.update_preview(net, data_layers_ids, all_layers_ids, layer_id)

    except CustomException as e:
        ui_utils.show_error("Error updating nodes", e)
        raise e
    except Exception as e:
        show_dialog(
            title="Error updating nodes", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise e
    finally:
        current_layers = g.layers.copy()
        for layer in current_layers.values():
            layer.set_preview_loading(False)


@handle_exception
def update_state():
    try:
        edges = nodes_flow.get_edges_json()
        nodes_state = nodes_flow.get_nodes_state_json()

        # Init layers data
        layers_ids = ui_utils.init_layers(nodes_state)
        all_layers_ids = layers_ids["all_layers_ids"]
        data_layers_ids = layers_ids["data_layers_ids"]
        labeling_jobs_layers_ids = [
            layer_id
            for layer_id in all_layers_ids
            if g.layers[layer_id].action.name.startswith(
                "create_labeling_job"
            )  # use action.name instead of hardcoded string
        ]

        # Init sources
        ui_utils.init_src(edges)

        # Calculate output metas for all layers
        utils.delete_results_dir()
        utils.create_results_dir()
        dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
        net = Net(dtl_json, g.RESULTS_DIR, g.MODALITY_TYPE)

        for layer_id in labeling_jobs_layers_ids:
            modifies_data = False
            parents = ui_utils.get_layer_parents_chain(layer_id)
            for parent in parents:
                net_layer = net.layers[all_layers_ids.index(parent)]
                modifies_data = modifies_data or net_layer.modifies_data()
            layer = g.layers[layer_id]
            layer.modifies_data(modifies_data)

        net.preview_mode = True
        ui_utils.init_nodes_state(net, data_layers_ids, all_layers_ids, nodes_state, edges)

    except CustomException as e:
        ui_utils.show_error("Error updating nodes", e)
        raise e
    except Exception as e:
        show_dialog(
            title="Error updating nodes", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise e


def update_nodes_cb():
    layer_sources = defaultdict(list)

    layers_to_update = []
    edges = nodes_flow.get_edges_json()
    for edge in edges:
        from_node_id = edge["output"]["node"]
        from_node_interface = edge["output"]["interface"]
        to_node_id = edge["input"]["node"]
        try:
            layer = g.layers[to_node_id]
        except:
            continue
        layer: Layer
        src_name = layer._connection_name(from_node_id, from_node_interface)
        layer_sources[to_node_id].append(src_name)

    for layer_id, layer in g.layers.items():
        layer: Layer
        if issubclass(layer.action, SourceAction):
            continue

        src_names = layer_sources[layer_id]

        layer_src = []
        for k in layer._src:
            try:
                layer_src.extend(layer._src[k])
            except:
                logger.info(f"Error in layer with ID: '{layer_id}'. layer._src: {layer._src}")

        if set(src_names) != set(layer_src):
            layers_to_update.append(layer.id)
    for layer_id in layers_to_update:
        g.updater(("nodes", layer_id))


def update_metas_cb():
    update_nodes_cb()
    g.updater("metas")


nodes_flow.flow_changed(update_nodes_cb)
nodes_flow.flow_state_changed(update_metas_cb)
nodes_flow.on_save(update_metas_cb)

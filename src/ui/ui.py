import json
from pathlib import Path
import queue
import random
import threading
import time
import traceback
from typing import Iterable
from supervisely.app.widgets import (
    Container,
    Select,
    Button,
    Flexbox,
    NodesFlow,
    Progress,
    Editor,
    Card,
    Text,
    ReloadableArea,
    TaskLogs,
)
from supervisely.app import show_dialog
from supervisely import ProjectMeta
from supervisely import logger
import supervisely as sly

from src.ui.dtl import actions_list, actions, Action
from src.ui.dtl.Layer import Layer
from src.ui.dtl import DATA_ACTIONS
from src.compute.main import main as compute_dtls
import src.globals as g
from src.compute.Net import Net
import src.utils as utils
from src.compute.layers.save.SuperviselyLayer import SuperviselyLayer


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
add_layer_btn = Button("Add Layer")
nodes_flow = NodesFlow(height="1000px")
run_btn = Button("Run", icon="zmdi zmdi-play")
json_editor = Editor(height_lines=100)
update_previews_btn = Button("Update previews")
save_json_button = Button("Save JSON")
load_json_button = Button("Load JSON")
json_editor_card = Card(
    title="DTL JSON",
    collapsable=True,
    content=json_editor,
    content_top_right=Flexbox(widgets=[save_json_button, load_json_button]),
)
json_editor_card.collapse()
progress = Progress(hide_on_finish=False)
add_layer_card = Card(
    title="Add new layer", content=Flexbox(widgets=[select_action_name, add_layer_btn])
)
download_archives_urls = Text("")
results = ReloadableArea()
results.hide()
nodes_flow_card = Card(
    title="DTL Graph",
    content=Container(widgets=[nodes_flow, run_btn, progress, results]),
    content_top_right=update_previews_btn,
)
layout_widgets = [
    add_layer_card,
    nodes_flow_card,
    json_editor_card,
]
logs = None
if not sly.is_development():
    logs = TaskLogs(sly.env.task_id())
    logs_card = Card(title="Logs", content=logs, collapsable=True)
    logs_card.collapse()
    layout_widgets.append(logs_card)

layout = Container(widgets=layout_widgets)


@save_json_button.click
def save_json_button_cb():
    edges = nodes_flow.get_edges_json()
    nodes_state = nodes_flow.get_nodes_state_json()

    # Init layers data
    layres_ids = utils.init_layers(nodes_state)
    all_layers_ids = layres_ids["all_layers_ids"]

    utils.init_src(edges)

    dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
    json_editor.set_text(json.dumps(dtl_json, indent=4), language_mode="json")
    json_editor_card.uncollapse()


def load_json():
    nodes_flow.loading = True
    try:
        # 1. read json
        try:
            dtl_json = json.loads(json_editor.get_text())
        except:
            show_dialog(
                title="Error",
                description="Invalid json",
                status="error",
            )
            nodes_flow.loading = False
            return
        if type(dtl_json) is not list:
            show_dialog(
                title="Error",
                description="Invalid json",
                status="error",
            )
            nodes_flow.loading = False
            return

        # create layer objects
        nodes_flow.clear()
        dst_to_layer_id = {}
        unknown_actions = set()
        missing_settings = set()
        bad_settings = set()
        ids = []
        layers_jsons_idxs = []
        data_layers_ids = []
        data_layer_id_to_json_idx = {}
        for i, layer_json in enumerate(dtl_json):
            action_name = layer_json.get("action", "__NO_ACTION__")
            try:
                action = actions.get(action_name)
            except:
                unknown_actions.add(action_name)
                continue
            settings = layer_json.get("settings", None)
            if settings is None:
                missing_settings.add(action_name)
                continue
            action: Action
            g.layers_count += 1
            id = action_name + "_" + str(g.layers_count)
            dst_layer = action.create_new_layer(id)
            g.layers[id] = dst_layer
            ids.append(id)
            if action_name in actions_list[DATA_ACTIONS]:
                data_layers_ids.append(id)
                data_layer_id_to_json_idx[id] = i
            layers_jsons_idxs.append(i)

        # create nodes
        for layer_id in ids:
            node = g.layers[layer_id].create_node()
            nodes_flow.add_node(node)

        # update src and dst
        for layer_id, json_idx in zip(ids, layers_jsons_idxs):
            layer_json = dtl_json[json_idx]
            layer = g.layers[layer_id]
            layer: Layer

            src = layer_json.get("src", [])
            if type(src) is str:
                src = [src]
            layer._src = src

            dst = layer_json.get("dst", [])
            if type(dst) is str:
                dst = [dst]
            layer._dst = dst

            for d in dst:
                dst_to_layer_id.setdefault(d, []).append(layer_id)

        # create node connections
        nodes_flow_edges = []
        for dst_layer_id in ids:
            dst_layer = g.layers[dst_layer_id]
            dst_layer: Layer
            for src in dst_layer.get_src():
                for src_layer_id in ids:
                    src_layer = g.layers[src_layer_id]
                    for dst_idx, dst in enumerate(src_layer.get_dst()):
                        if dst == src:
                            try:
                                nodes_flow_edges.append(
                                    {
                                        "id": random.randint(10000000000000, 99999999999999),
                                        "output": {
                                            "node": src_layer_id,
                                            "interface": src_layer.get_destination_name(dst_idx),
                                        },
                                        "input": {
                                            "node": dst_layer_id,
                                            "interface": "source",
                                        },
                                    }
                                )
                            except:
                                pass
        nodes_flow.set_edges(nodes_flow_edges)

        # get metas for data layers
        # PROBLEM: nodes_flow_state is empty. need to get post request from client to update StateJson
        nodes_flow_state = nodes_flow.get_flow_state()
        input_metas = {}
        for layer_id in data_layers_ids:
            data_layer = g.layers[layer_id]
            src = data_layer.get_src()
            if src is None or len(src) == 0:
                # Skip if no sources specified for data layer
                continue

            # Add project meta
            project_name, dataset_name = src[0].split("/")
            project_info = utils.get_project_by_name(project_name)
            project_meta = utils.get_project_meta(project_info.id)
            input_metas[project_name] = project_meta

            data_layer.meta_changed_cb(project_meta)
            layer_json = dtl_json[data_layer_id_to_json_idx[layer_id]]
            try:
                new_state = data_layer.set_settings_from_json(layer_json, {})
                if new_state is not None and len(new_state) > 0:
                    nodes_flow_state[layer_id] = new_state
            except:
                logger.debug(
                    "Error setting settings from json for data layer",
                    exc_info=traceback.format_exc(),
                )
                bad_settings.add(data_layer.action.name)
                continue

        net = Net(dtl_json, g.RESULTS_DIR)
        net.calc_metas()
        for layer_id, net_layer in zip(ids, net.layers):
            g.layers[layer_id].output_meta = net_layer.output_meta

        # update settings
        for layer_id, json_idx, net_layer in zip(ids, layers_jsons_idxs, net.layers):
            layer_json = dtl_json[json_idx]
            layer = g.layers[layer_id]

            # update settings
            if layer.action.name not in actions_list[DATA_ACTIONS]:
                layer_input_meta = ProjectMeta()
                for src in layer.get_src():
                    src_layer_id = utils.find_layer_id_by_dst(src)
                    if src_layer_id is None:
                        continue
                    src_layer = g.layers[src_layer_id]
                    if src_layer.output_meta is not None:
                        layer_input_meta = utils.merge_input_metas(
                            [layer_input_meta, src_layer.output_meta]
                        )
                if layer.meta_changed_cb is not None:
                    layer.meta_changed_cb(layer_input_meta)
                try:
                    # state = nodes_flow_state[layer_id]
                    new_state = layer.set_settings_from_json(layer_json, {})
                    if new_state is not None:
                        nodes_flow_state[layer_id] = new_state
                except:
                    logger.debug(
                        "Error updating settings from json", exc_info=traceback.format_exc()
                    )
                    bad_settings.add(layer.action.name)
                    continue

        nodes_flow.update_nodes_state(nodes_flow_state)

        def actions_str(actions: Iterable):
            return ", ".join([f'"{a}"' for a in actions])

        problems_reading = (
            f"Actions {actions_str(unknown_actions)} not found. "
            if len(unknown_actions) > 0
            else ""
        )
        problems_reading += (
            f"Missing settings in actions: {actions_str(missing_settings)}. "
            if len(missing_settings) > 0
            else ""
        )
        problems_reading += (
            f"Bad settings in actions: {actions_str(bad_settings)}" if len(bad_settings) > 0 else ""
        )
        if len(problems_reading) > 0:
            show_dialog(
                title="Errors reading from json",
                description=problems_reading,
                status="warning",
            )
    except:
        logger.debug("Error loading json", exc_info=traceback.format_exc())
    finally:
        nodes_flow.loading = False


@add_layer_btn.click
def add_layer_btn_cb():
    action_name = select_action_name.get_value()
    try:
        action = actions.get(action_name)
    except:
        show_dialog(
            title="Error",
            description=f"Action {action_name} not found",
            status="error",
        )
        return
    action: Action
    g.layers_count += 1
    id = action_name + "_" + str(g.layers_count)
    layer = action.create_new_layer(id)
    g.layers[id] = layer
    node = layer.create_node()
    nodes_flow.add_node(node)


@run_btn.click
def run():
    edges = nodes_flow.get_edges_json()
    nodes_state = nodes_flow.get_nodes_state_json()

    run_btn.hide()
    progress.show()
    results.hide()

    try:
        # init layers
        try:
            utils.init_layers(nodes_state)
        except Exception as e:
            show_dialog(
                title="Error parsing settings",
                description=f"{type(e).__name__}: {str(e)}",
                status="error",
            )
            raise

        # init layers sources
        # destinations are defined in init_layers
        try:
            utils.init_src(edges)
        except Exception as e:
            show_dialog(
                title="Error parsing connections",
                description=f"{type(e).__name__}: {str(e)}",
                status="error",
            )
            raise

        utils.delete_results_dir()
        utils.create_results_dir()
        utils.delete_data_dir()
        utils.create_data_dir()

    except:
        logger.debug("Error initializing layers", exc_info=traceback.format_exc())
        progress.hide()
        run_btn.show()
        return
    try:
        dtl_json = [g.layers[node_id].to_json() for node_id in nodes_state]
        utils.save_dtl_json(dtl_json)
        net = compute_dtls(progress)
    except:
        logger.debug("Error computing dtls", exc_info=traceback.format_exc())
    file_infos = []
    with progress(
        total=len([p for p in Path(g.RESULTS_DIR).iterdir() if p.is_dir()]),
        message="Uploading result projects...",
    ) as pbar:
        for pr_dir in Path(g.RESULTS_DIR).iterdir():
            if pr_dir.is_dir():
                try:
                    tar_path = str(pr_dir) + ".tar"
                    sly.fs.archive_directory(pr_dir, tar_path)
                    file_info = g.api.file.upload(
                        g.TEAM_ID,
                        src=tar_path,
                        dst=f"/dtl/{utils.get_task()}/{Path(tar_path).name}",
                        # progress_cb=progress(),
                    )
                    file_infos.append(file_info)
                    if not sly.is_development():
                        g.api.task.set_output_archive(
                            sly.env.task_id(), file_info.id, file_info.name
                        )
                except Exception as e:
                    logger.debug("Error uploading results", exc_info=traceback.format_exc())
                    show_dialog(title="Error uploading results", description=str(e), status="error")
                finally:
                    pbar.update()
    try:
        supervisely_layers = [l for l in net.layers if isinstance(l, SuperviselyLayer)]
        results.set_content(utils.create_results_widget(file_infos, supervisely_layers))
        results.reload()
        results.show()
    except:
        pass
    finally:
        progress.hide()
        run_btn.show()


def update_nodes():
    nodes_flow.loading = True
    try:
        edges = nodes_flow.get_edges_json()
        nodes_state = nodes_flow.get_nodes_state_json()

        # Init layers data
        layers_ids = utils.init_layers(nodes_state)
        data_layers_ids = layers_ids["data_layers_ids"]
        all_layers_ids = layers_ids["all_layers_ids"]

        # Init sources
        utils.init_src(edges)

        # Calculate output metas for all layers
        utils.delete_results_dir()
        utils.create_results_dir
        dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
        net = Net(dtl_json, g.RESULTS_DIR)
        utils.init_output_metas(net, all_layers_ids)

        # Call meta changed callbacks to update ui
        for layer_id in all_layers_ids:
            layer = g.layers[layer_id]
            if layer.action.name not in actions_list[DATA_ACTIONS]:
                layer_input_meta = ProjectMeta()
                for src in layer.get_src():
                    src_layer_id = utils.find_layer_id_by_dst(src)
                    src_layer = g.layers[src_layer_id]
                    if src_layer.output_meta is not None:
                        layer_input_meta = utils.merge_input_metas(
                            [layer_input_meta, src_layer.output_meta]
                        )
                layer.meta_changed_cb(layer_input_meta)

        # Load preview for data layers
        utils.delete_preview_dir()
        utils.create_preview_dir()
        utils.set_preview(data_layers_ids)

        # Update preview
        utils.update_previews(net, data_layers_ids, all_layers_ids)

    except:
        logger.debug("Error updating nodes", exc_info=traceback.format_exc())
        show_dialog(title="Error", description="Error updating nodes", status="error")
    finally:
        nodes_flow.loading = False


def update_metas():
    try:
        edges = nodes_flow.get_edges_json()
        nodes_state = nodes_flow.get_nodes_state_json()

        # Init layers data
        layers_ids = utils.init_layers(nodes_state)
        all_layers_ids = layers_ids["all_layers_ids"]

        # Init sources
        utils.init_src(edges)

        # Calculate output metas for all layers
        utils.delete_results_dir()
        utils.create_results_dir
        dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
        net = Net(dtl_json, g.RESULTS_DIR)
        utils.init_output_metas(net, all_layers_ids)

        # Call meta changed callbacks to update ui
        for layer_id in all_layers_ids:
            layer = g.layers[layer_id]
            if layer.action.name not in actions_list[DATA_ACTIONS]:
                layer_input_meta = ProjectMeta()
                for src in layer.get_src():
                    src_layer_id = utils.find_layer_id_by_dst(src)
                    src_layer = g.layers[src_layer_id]
                    if src_layer.output_meta is not None:
                        layer_input_meta = utils.merge_input_metas(
                            [layer_input_meta, src_layer.output_meta]
                        )
                layer.meta_changed_cb(layer_input_meta)

    except:
        logger.debug("Error updating metas", exc_info=traceback.format_exc())


_update_queue = queue.Queue()


def _update_f():
    global _update_queue
    while True:
        updates = []
        while not _update_queue.empty():
            updates.append(_update_queue.get())
        if len(updates) == 0:
            time.sleep(0.1)
            continue
        try:
            if "load_json" in updates:
                load_json()
            elif "nodes" in updates:
                update_nodes()
            else:
                update_metas()
        finally:
            for _ in range(len(updates)):
                _update_queue.task_done()
        time.sleep(0.1)


_update_loop = threading.Thread(
    target=_update_f,
    name="App update loop",
    daemon=True,
).start()


def updater(update: str):
    global _update_queue
    _update_queue.put(update)


def update_nodes_cb():
    updater("nodes")


def update_metas_cb():
    updater("metas")


def load_json_cb():
    updater("load_json")


nodes_flow.flow_changed(update_metas_cb)
nodes_flow.flow_state_changed(update_metas_cb)
nodes_flow.on_save(update_nodes_cb)
update_previews_btn.click(update_nodes_cb)
load_json_button.click(load_json_cb)

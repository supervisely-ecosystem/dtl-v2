import random
import json

from supervisely.app.widgets import (
    Button,
    Editor,
    Container,
    Flexbox,
    TeamFilesSelector,
    Input,
    Card,
    NotificationBox,
    Select,
    OneOf,
    Empty,
)
from supervisely.app import show_dialog

from src.compute.Net import Net
from src.ui.dtl.Layer import Layer
from src.ui.dtl import actions_list
from src.ui.dtl import SOURCE_ACTIONS
from src.ui.tabs.configure import nodes_flow
import src.ui.utils as ui_utils
import src.utils as utils
import src.globals as g
from src.exceptions import handle_exception
from src.exceptions import CustomException, BadSettingsError

preset_name_input = Input(placeholder="Preset name")
save_folder_selector = TeamFilesSelector(
    team_id=g.TEAM_ID, selection_file_type="folder", max_height=254
)
save_preset_btn = Button("Save", icon="zmdi zmdi-floppy")
save_notification_saved = NotificationBox("Preset saved", box_type="success")
save_notification_empty_name = NotificationBox("Empty preset name", box_type="error")
save_notification_empty_folder = NotificationBox("Save directory not selected", box_type="error")
save_notification_select = Select(
    items=[
        Select.Item("empty", content=Empty()),
        Select.Item("saved", content=save_notification_saved),
        Select.Item("empty_name", content=save_notification_empty_name),
        Select.Item("empty_folder", content=save_notification_empty_folder),
    ]
)
save_notification_oneof = OneOf(save_notification_select)
save_container = Container(
    widgets=[
        preset_name_input,
        save_folder_selector,
        Flexbox(
            widgets=[
                save_preset_btn,
                save_notification_oneof,
            ],
            gap=20,
        ),
    ]
)

load_file_selector = TeamFilesSelector(
    team_id=g.TEAM_ID, selection_file_type="file", max_height=300
)
load_preset_btn = Button("Load")
load_notification_loaded = NotificationBox("Preset loaded", box_type="success")
load_notification_file_not_selected = NotificationBox("File not selected", box_type="error")
load_notification_applied = NotificationBox("Preset applied", box_type="success")
load_notification_select = Select(
    items=[
        Select.Item("empty", content=Empty()),
        Select.Item("loaded", content=load_notification_loaded),
        Select.Item("not selected", content=load_notification_file_not_selected),
        Select.Item("applied", content=load_notification_applied),
    ]
)
load_notification_oneof = OneOf(load_notification_select)
apply_preset = Button("Apply", style="margin: 0")
load_container = Container(
    widgets=[
        load_file_selector,
        Flexbox(widgets=[load_preset_btn, apply_preset, load_notification_oneof], gap=20),
    ]
)

json_editor = Editor(language_mode="json", height_px=300)
json_editor_card = Card(title="JSON Preview", content=json_editor, collapsable=True)
json_editor_card.collapse()

save_layout = Container(widgets=[save_container, json_editor], gap=0)
load_layout = Container(widgets=[load_container, json_editor], gap=0)


@save_preset_btn.click
def save_json_button_cb():
    edges = nodes_flow.get_edges_json()
    nodes_state = nodes_flow.get_nodes_state_json()

    # Init layers data
    layres_ids = ui_utils.init_layers(nodes_state)
    all_layers_ids = layres_ids["all_layers_ids"]

    ui_utils.init_src(edges)

    dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
    json_editor.set_text(json.dumps(dtl_json, indent=4), language_mode="json")

    preset_name = preset_name_input.get_value()
    if preset_name == "":
        preset_name = preset_name_input.get_value("empty_name")
        return
    save_paths = save_folder_selector.get_selected_paths()
    if len(save_paths) == 0:
        preset_name = preset_name_input.get_value("empty_folder")
        return
    dst_path = save_paths[0] + "/" + preset_name + ".json"
    src_path = g.DATA_DIR + "/preset.json"
    with open(src_path, "w") as f:
        json.dump(dtl_json, f, indent=4)
    g.api.file.upload(g.TEAM_ID, src_path, dst_path)
    save_notification_select.set_value("saved")


@load_preset_btn.click
def load_json_button_cb():
    paths = load_file_selector.get_selected_paths()
    if len(paths) == 0:
        load_notification_select.set_value("not selected")
        return
    g.api.file.download(g.TEAM_ID, paths[0], g.DATA_DIR + "/preset.json")
    with open(g.DATA_DIR + "/preset.json", "r") as f:
        json_editor.set_text(f.read(), language_mode="json")
    load_notification_select.set_value("loaded")


@handle_exception
def apply_json():
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
                description="Invalid json. Must be list of layers",
                status="error",
            )
            nodes_flow.loading = False
            return

        # create layer objects
        nodes_flow.clear()
        ids = []
        data_layers_ids = []
        for layer_json in dtl_json:
            action_name = layer_json.get("action", None)
            if action_name is None:
                raise BadSettingsError(
                    'Missing "action" field in layer config', extra={"layer_config": layer_json}
                )
            settings = layer_json.get("settings", None)
            if settings is None:
                raise BadSettingsError(
                    'Missing "settings" field in layer config', extra={"layer_config": layer_json}
                )

            layer = ui_utils.create_new_layer(action_name)
            ids.append(layer.id)
            if action_name in actions_list[SOURCE_ACTIONS]:
                data_layers_ids.append(layer.id)

        # update src and dst
        for i, layer_id in enumerate(ids):
            layer_json = dtl_json[i]
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

        # update settings
        for i, layer_id in enumerate(ids):
            layer_json = dtl_json[i]
            layer = g.layers[layer_id]
            layer.from_json(layer_json)

        # init metas for data layers
        for i, layer_id in enumerate(data_layers_ids):
            data_layer = g.layers[layer_id]
            src = data_layer.get_src()
            if len(src) == 0:
                # Skip if no sources specified for data layer
                continue

            # Add project meta
            try:
                project_name, dataset_name = src[0].split("/")
            except:
                raise BadSettingsError(
                    'Wrong "data" layer source path. Use "project_name/dataset_name" or "project_name/*"',
                    extra={"layer_config": dtl_json[i]},
                )
            try:
                project_info = utils.get_project_by_name(project_name)
                project_meta = utils.get_project_meta(project_info.id)
            except Exception as e:
                raise CustomException(
                    f"Error getting project meta", error=e, extra={"project_name": project_name}
                )
            data_layer.update_project_meta(project_meta)

        # init metas for all layers
        net = Net(dtl_json, g.RESULTS_DIR)
        net.calc_metas()
        for layer_id, net_layer in zip(ids, net.layers):
            layer = g.layers[layer_id]
            layer: Layer
            layer.output_meta = net_layer.output_meta

        for layer_id in ids:
            if layer_id in data_layers_ids:
                continue
            layer = g.layers[layer_id]
            layer_input_meta = utils.merge_input_metas(
                [
                    g.layers[ui_utils.find_layer_id_by_dst(src)].output_meta
                    for src in layer.get_src()
                ]
            )
            layer.update_project_meta(layer_input_meta)

        # create nodes
        for layer_id in ids:
            layer = g.layers[layer_id]
            node = layer.create_node()
            nodes_flow.add_node(node)

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
        load_notification_select.set_value("applied")

    except CustomException as e:
        ui_utils.show_error("Error loading json", e)
        raise e
    except Exception as e:
        show_dialog(
            title="Error loading json", description=f"Unexpected Error: {str(e)}", status="error"
        )
        raise e
    finally:
        nodes_flow.loading = False


def load_json_cb():
    g.updater("load_json")


apply_preset.click(load_json_cb)

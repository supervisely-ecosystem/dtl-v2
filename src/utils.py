from collections import namedtuple
from typing import Callable, List, Optional, Tuple, Union
import json
import os
import shutil
from tqdm import tqdm
from src.compute.dtl_utils.image_descriptor import ImageDescriptor
import supervisely as sly

import src.globals as g
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import Flexbox, Text, ProjectThumbnail, FileThumbnail, Container


def download_data(
    project_name: str,
    dataset_names: Union[str, None],
    progress_cb: Optional[Union[tqdm, Callable]] = None,
):
    """
    Download Project and Datasets from Supervisely to local storage
    :param project_name: name of project to download
    :param dataset_names: name of datasets to download. If None, download all datasets
    :param progress_cb: progress callback
    """
    project_info = get_project_by_name(project_name)
    if project_info is None:
        raise RuntimeError(f"Project {project_name} not found")
    if dataset_names is None:
        datasets_ids = [ds.id for ds in g.api.dataset.get_list(project_info.id)]
    else:
        datasets_ids = []
        for dataset_name in dataset_names:
            dataset_info = get_dataset_by_name(dataset_name, project_info.id)
            if dataset_info is None:
                raise RuntimeError(f"Dataset {dataset_name} not found in project {project_name}")
            datasets_ids.append(dataset_info.id)
    sly.download_project(
        g.api,
        project_info.id,
        f"{g.DATA_DIR}/{project_name}",
        dataset_ids=datasets_ids,
        progress_cb=progress_cb,
        save_images=True,
    )


def download_preview(project_name, dataset_name) -> Tuple[str, str]:
    project_info = get_project_by_name(project_name)
    if project_info is None:
        raise RuntimeError(f"Project {project_name} not found")
    if dataset_name == "*":
        dataset_info = get_all_datasets(project_info.id)[0]
        dataset_name = dataset_info.name
    else:
        dataset_info = get_dataset_by_name(dataset_name, project_info.id)
    if dataset_info is None:
        raise RuntimeError(f"Dataset {dataset_name} not found in project {project_name}")
    preview_project_path = f"{g.PREVIEW_DIR}/{project_name}"
    preview_dataset_path = f"{preview_project_path}/{dataset_name}"
    ensure_dir(preview_dataset_path)
    image_id = g.api.image.get_list(dataset_info.id, limit=1)[0].id
    preview_img_path = f"{preview_dataset_path}/preview_image.jpg"
    g.api.image.download(image_id, preview_img_path)
    ann_json = g.api.annotation.download_json(image_id)
    preview_ann_path = f"{preview_dataset_path}/preview_ann.json"
    with open(preview_ann_path, "w") as f:
        json.dump(ann_json, f)

    return preview_img_path, preview_ann_path


def _get_project_by_name_or_id(name: str = None, id: int = None):
    if id is None:
        if name is None:
            raise ValueError("name or id must be specified")
        if name not in g.cache["project_id"]:
            try:
                project_info = g.api.project.get_info_by_name(
                    g.WORKSPACE_ID, name, raise_error=True
                )
            except:
                raise RuntimeError(f"Project {name} not found")
            g.cache["project_info"][project_info.id] = project_info
            g.cache["project_id"][name] = project_info.id
        project_id = g.cache["project_id"][name]
        return g.cache["project_info"][project_id]
    if id not in g.cache["project_info"]:
        try:
            project_info = g.api.project.get_info_by_id(
                id, expected_type=sly.ProjectType.IMAGES, raise_error=True
            )
        except:
            raise RuntimeError(f"Project {id} not found")
        g.cache["project_info"][id] = project_info
        g.cache["project_id"][project_info.name] = project_info.id
    return g.cache["project_info"][id]


def get_project_by_name(name: str) -> sly.ProjectInfo:
    return _get_project_by_name_or_id(name=name)


def get_project_by_id(id: int) -> sly.ProjectInfo:
    return _get_project_by_name_or_id(id=id)


def get_dataset_by_id(id: int = None) -> sly.DatasetInfo:
    if id not in g.cache["dataset_info"]:
        try:
            dataset_info = g.api.dataset.get_info_by_id(id, raise_error=True)
        except:
            raise RuntimeError(f"Dataset {id} not found")
        g.cache["dataset_info"][id] = dataset_info
        g.cache["dataset_id"][(dataset_info.project_id, dataset_info.name)] = dataset_info.id
    return g.cache["dataset_info"][id]


def get_dataset_by_name(dataset_name: str, project_id: int) -> sly.DatasetInfo:
    key = (project_id, dataset_name)
    if key not in g.cache["dataset_id"]:
        try:
            dataset_info = g.api.dataset.get_info_by_name(project_id, dataset_name)
        except:
            raise RuntimeError(f"Dataset {dataset_name} not found")
        g.cache["dataset_info"][dataset_info.id] = dataset_info
        g.cache["dataset_id"][key] = dataset_info.id
    dataset_id = g.cache["dataset_id"][key]
    return g.cache["dataset_info"][dataset_id]


def get_project_meta(project_id: int):
    if project_id not in g.cache["project_meta"]:
        try:
            project_meta_json = g.api.project.get_meta(project_id)
        except:
            raise RuntimeError(f"Project {project_id} not found")
        project_meta = sly.ProjectMeta.from_json(project_meta_json)
        g.cache["project_meta"][project_id] = project_meta
    return g.cache["project_meta"][project_id]


def merge_input_metas(input_metas: List[sly.ProjectMeta]) -> sly.ProjectMeta:
    full_input_meta = sly.ProjectMeta()
    for inp_meta in input_metas:
        for inp_obj_class in inp_meta.obj_classes:
            existing_obj_class = full_input_meta.obj_classes.get(inp_obj_class.name, None)
            if existing_obj_class is None:
                full_input_meta = full_input_meta.add_obj_class(inp_obj_class)
            elif existing_obj_class.geometry_type != inp_obj_class.geometry_type:
                raise RuntimeError(
                    f"Trying to add new class ({inp_obj_class.name}) with shape ({inp_obj_class.geometry_type.geometry_name()}). Same class with different shape ({existing_obj_class.geometry_type.geometry_name()}) exists."
                )
        for inp_tag_meta in inp_meta.tag_metas:
            existing_tag_meta = full_input_meta.tag_metas.get(inp_tag_meta.name, None)
            if existing_tag_meta is None:
                full_input_meta = full_input_meta.add_tag_meta(inp_tag_meta)
            elif not existing_tag_meta.is_compatible(inp_tag_meta):
                raise RuntimeError(
                    f"Trying to add new tag ({inp_tag_meta.name}) with type ({inp_tag_meta.value_type}) and possible values ({inp_tag_meta.possible_values}). Same tag with different type ({existing_tag_meta.value_type}) or possible values ({existing_tag_meta.possible_values}) exists."
                )
    return full_input_meta


def get_all_datasets(project_id: int) -> List[sly.DatasetInfo]:
    if project_id not in g.cache["all_datasets"]:
        datasets = g.api.dataset.get_list(project_id)
        g.cache["all_datasets"][project_id] = [dataset.id for dataset in datasets]
        g.cache["dataset_info"].update(
            {
                dataset.id: dataset
                for dataset in datasets
                if dataset.id not in g.cache["dataset_info"]
            }
        )
    return [get_dataset_by_id(ds_id) for ds_id in g.cache["all_datasets"][project_id]]


def find_layer_id_by_dst(dst: str):
    for layer_id, layer in g.layers.items():
        if dst in layer.get_dst():
            return layer_id
    return None
    # return name.lstrip("$").split("__")[0]


def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def delete_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=False)


def save_dtl_json(dtl_json):
    ensure_dir("sly_task_data")
    with open("sly_task_data/graph.json", "w") as f:
        json.dump(dtl_json, f, indent=4)


def delete_results_dir():
    delete_dir(g.RESULTS_DIR)


def create_results_dir():
    ensure_dir(g.RESULTS_DIR)


def delete_data_dir():
    delete_dir(g.DATA_DIR)


def create_data_dir():
    ensure_dir(g.DATA_DIR)


def delete_preview_dir():
    delete_dir(g.PREVIEW_DIR)


def create_preview_dir():
    ensure_dir(g.PREVIEW_DIR)


def init_layers(nodes_state: dict):
    from src.ui.dtl import DATA_ACTIONS, SAVE_ACTIONS, TRANSFORMATION_ACTIONS, actions_list

    data_layers_ids = []
    save_layers_ids = []
    transform_layers_ids = []
    all_layers_ids = []
    for node_id, node_options in nodes_state.items():
        layer = g.layers[node_id]
        layer: Layer

        layer.clear()
        layer.parse_options(node_options)

        if layer.action.name in actions_list[DATA_ACTIONS]:
            data_layers_ids.append(node_id)
        if layer.action.name in actions_list[SAVE_ACTIONS]:
            save_layers_ids.append(node_id)
        if layer.action.name in actions_list[TRANSFORMATION_ACTIONS]:
            transform_layers_ids.append(node_id)
        all_layers_ids.append(node_id)

    return {
        "data_layers_ids": data_layers_ids,
        "save_layers_ids": save_layers_ids,
        "transformation_layers_ids": transform_layers_ids,
        "all_layers_ids": all_layers_ids,
    }


def init_src(edges: list):
    for edge in edges:
        from_node_id = edge["output"]["node"]
        from_node_interface = edge["output"]["interface"]
        to_node_id = edge["input"]["node"]
        layer = g.layers[to_node_id]
        layer: Layer
        layer.add_source(from_node_id, from_node_interface)


def get_input_metas(data_layers_ids):
    input_metas = {}
    for data_layer_id in data_layers_ids:
        data_layer = g.layers[data_layer_id]
        src = data_layer.get_src()
        if src is None or len(src) == 0:
            # Skip if no sources specified for data layer
            continue

        project_name, _ = src[0].split("/")
        project_info = get_project_by_name(project_name)
        project_meta = get_project_meta(project_info.id)
        input_metas[project_name] = project_meta

    return input_metas


def set_preview(data_layers_ids):
    for data_layer_id in data_layers_ids:
        data_layer = g.layers[data_layer_id]
        src = data_layer.get_src()
        if src is None or len(src) == 0:
            # Skip if no sources specified for data layer
            continue

        project_name, dataset_name = src[0].split("/")
        project_info = get_project_by_name(project_name)
        project_meta = get_project_meta(project_info.id)

        preview_img_path, preview_ann_path = download_preview(project_name, dataset_name)
        preview_img = sly.image.read(preview_img_path)
        with open(preview_ann_path, "r") as f:
            preview_ann = sly.Annotation.from_json(json.load(f), project_meta)
        data_layer.set_preview(preview_img, preview_ann)


def init_output_metas(net, all_layers_ids: list):
    net.calc_metas()
    for layer_id, net_layer in zip(all_layers_ids, net.layers):
        g.layers[layer_id].output_meta = net_layer.output_meta


LegacyProjectItem = namedtuple(
    "LegacyProjectItem",
    [
        "project_name",
        "ds_name",
        "image_name",
        "ia_data",
        "img_path",
        "ann_path",
    ],
)


def update_previews(net, data_layers_ids: list, all_layers_ids: list):
    updated = set()
    net.preprocess()
    for data_layer_id in data_layers_ids:
        data_layer = g.layers[data_layer_id]
        src = data_layer.get_src()
        project_name, dataset_name = src[0].split("/")
        if dataset_name == "*":
            dataset_name = get_all_datasets(get_project_by_name(project_name).id)[0].name
        preview_path = f"{g.PREVIEW_DIR}/{project_name}/{dataset_name}"

        img_desc = ImageDescriptor(
            LegacyProjectItem(
                project_name=project_name,
                ds_name=dataset_name,
                image_name="preview_image",
                ia_data={"image_ext": ".jpg"},
                img_path=f"{preview_path}/preview_image.jpg",
                ann_path=f"{preview_path}/preview_ann.json",
            ),
            False,
        )
        ann = data_layer.get_ann()
        data_el = (img_desc, ann)

        processing_generator = net.start_iterate(data_el)
        for data_el, layer_indx in processing_generator:
            if layer_indx in updated:
                continue
            layer = g.layers[all_layers_ids[layer_indx]]
            layer: Layer
            if len(data_el) == 1:
                img_desc, ann = data_el[0]
            elif len(data_el) == 3:
                img_desc, ann, _ = data_el
            else:
                img_desc, ann = data_el
            layer.set_preview(img_desc.read_image(), ann)
            updated.add(layer_indx)


def create_url_html(url, name):
    return f'<a href="{url}" target="_blank">{name}</a>'


def create_urls_text(urls: List[Tuple[str, str]]):
    return f"<div>{''.join([create_url_html(*x) for x in urls])}</div>"


def get_task():
    task_id = os.environ.get("TASK_ID", None)
    if task_id is None:
        return "local"
    return task_id


def get_workspace_by_id(workspace_id) -> sly.WorkspaceInfo:
    if workspace_id not in g.cache["workspace_info"]:
        try:
            workspace_info = g.api.workspace.get_info_by_id(workspace_id)
        except:
            raise RuntimeError(f"Workspace {workspace_id} not found")
        g.cache["workspace_info"][workspace_id] = workspace_info
    return g.cache["workspace_info"][workspace_id]


def update_project_info(project_info: sly.ProjectInfo):
    updated = g.api.project.get_info_by_id(project_info.id)
    g.cache["project_info"][project_info.id] = updated
    return updated


def create_results_widget(file_infos, supervisely_layers):
    widgets = []
    if len(file_infos) > 0:
        widgets.append(
            Flexbox(
                widgets=[
                    Text("Archives: "),
                    *[FileThumbnail(file_info) for file_info in file_infos],
                ]
            )
        )
    if len(supervisely_layers) > 0:
        widgets.append(
            Flexbox(
                widgets=[
                    Text("Projects: "),
                    *[
                        ProjectThumbnail(update_project_info(l.sly_project_info))
                        for l in supervisely_layers
                    ],
                ]
            )
        )
    return Container(widgets=widgets)

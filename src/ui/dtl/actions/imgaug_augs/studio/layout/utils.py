from typing import List
from supervisely.api.api import Api
from supervisely.app.widgets import (
    AgentSelector,
    Button,
    Text,
    Select,
    RadioTabs,
    RadioGroup,
    CustomModelsSelector,
    PretrainedModelsSelector,
    Checkbox,
)

from supervisely.api.agent_api import AgentInfo
from supervisely.api.app_api import SessionInfo
import src.globals as g
import supervisely as sly
import os
from collections import OrderedDict
from cache import get_random_image

augs_configs = sly.json.load_json_file(os.path.join(os.getcwd(), "augs.json"))
meta = g.api.project.get_meta(g.PROJECT_ID)

pipeline = []

images_info = {}
all_images = []


def _normalize_params(default_params: dict, params: dict):
    ptypes = {p["pname"]: p for p in default_params}
    res = OrderedDict()
    for name, value in params.items():
        if ptypes[name]["type"] == "el-slider-range":
            res[name] = tuple(value)
        elif (
            ptypes[name]["type"] == "el-input-number" and ptypes[name].get("valueType") is not None
        ):
            try:
                res[name] = int(value)
            except ValueError as e:
                res[name] = int(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-number":
            try:
                res[name] = float(value)
            except ValueError as e:
                res[name] = float(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-range":
            try:
                res[name] = tuple([int(value[0]), int(value[1])])
            except ValueError as e:
                res[name] = tuple(ptypes[name]["default"])
        elif ptypes[name]["type"] == "el-input-number-range":
            try:
                res[name] = [int(value[0]), int(value[1])]
                res[name].sort()
                res[name] = tuple(res[name])
            except ValueError as e:
                res[name] = tuple(ptypes[name]["default"])
        else:
            res[name] = value
    return res


def get_aug_info(state):
    category_name = state["category"]
    aug_name = state["aug"]
    ui_defaults = augs_configs[category_name][aug_name]["params"]
    ui_vmodels = state["augVModels"][category_name][aug_name]
    sometimes = float(state["sometimesP"]) if state["sometimes"] else None
    params = _normalize_params(ui_defaults, ui_vmodels)
    aug_info = sly.imgaug_utils.create_aug_info(category_name, aug_name, params, sometimes)
    return aug_info


def save_preview_image(api: sly.Api, task_id, img):
    local_path = g.PREVIEW_DIR
    remote_path = os.path.join(f"/imgaug_studio/{task_id}", f"last_preview.png")
    sly.image.write(local_path, img)
    if api.file.exists(g.TEAM_ID, remote_path):
        api.file.remove(g.TEAM_ID, remote_path)
    file_info = api.file.upload(g.TEAM_ID, local_path, remote_path)
    return file_info


def preview_augs(api: sly.Api, task_id, augs, infos, py_code=None):
    img_info, img = get_random_image(api)
    ann_json = api.annotation.download(img_info.id).annotation
    ann = sly.Annotation.from_json(ann_json, meta)

    try:
        res_meta, res_img, res_ann = sly.imgaug_utils.apply(augs, meta, img, ann)
    except ValueError as e:
        if str(e) == "cannot convert float NaN to integer":
            e.args = ("Please check the values of the augmentation parameters",)
            raise e
        else:
            raise e
    file_info = save_preview_image(api, task_id, res_img)
    _labels_new_classes = []
    _new_classes = {}
    for label in ann.labels:
        label: sly.Label
        if type(label.obj_class.geometry_type) is sly.Rectangle:
            new_name = f"{label.obj_class.name}_polygon_for_gallery"
            if new_name not in _new_classes:
                _new_classes[new_name] = label.obj_class.clone(name=new_name)
            _labels_new_classes.append(label.clone(obj_class=_new_classes[new_name]))
        else:
            _labels_new_classes.append(label.clone())
    _meta_renamed_polygons = sly.ProjectMeta(
        obj_classes=sly.ObjClassCollection(list(_new_classes.values()))
    )
    gallery_meta = res_meta.merge(_meta_renamed_polygons)
    # cheat code ############################################

    gallery, sync_keys = get_gallery(
        project_meta=gallery_meta,
        urls=[img_info.path_original, file_info.storage_path],
        card_names=["original", "augmented"],
        img_labels=[_labels_new_classes, res_ann.labels],
    )
    fields = [
        {"field": "data.gallery", "payload": gallery},
        {"field": "state.galleryOptions.syncViewsBindings", "payload": sync_keys},
        {"field": "state.previewPipelineLoading", "payload": False},
        {"field": "state.previewAugLoading", "payload": False},
    ]
    if len(infos) == 1 and py_code is None:
        fields.append({"field": "state.previewPy", "payload": infos[0]["python"]})
    else:
        if py_code is None:
            py_code = sly.imgaug_utils.pipeline_to_python(infos, random_order=False)
        fields.append({"field": "state.previewPy", "payload": py_code})
    api.task.set_fields(task_id, fields)


def get_gallery(project_meta: sly.ProjectMeta, urls, card_names, img_labels=None):
    if img_labels is None:
        img_labels = [[]] * len(urls)

    if len(urls) % 2 != 0:
        raise ValueError("Gallery only for image pairs")

    CNT_GRID_COLUMNS, gallery = get_empty_gallery(project_meta)

    grid_annotations = {}
    grid_layout = [[] for i in range(CNT_GRID_COLUMNS)]
    sync_keys = [[] for i in range(int((len(urls) / 2)))]
    for idx, (image_url, card_name, labels) in enumerate(zip(urls, card_names, img_labels)):
        grid_annotations[str(idx)] = {
            "url": image_url,
            "figures": [label.to_json() for label in labels],
            "info": {"title": card_name},
        }
        grid_layout[idx % CNT_GRID_COLUMNS].append(str(idx))
        sync_keys[int(idx / 2)].append(str(idx))

    gallery["content"]["layout"] = grid_layout
    gallery["content"]["annotations"] = grid_annotations
    return gallery, sync_keys


def get_empty_gallery(meta: sly.ProjectMeta = sly.ProjectMeta()):
    CNT_GRID_COLUMNS = 2
    empty_gallery = {
        "content": {
            "projectMeta": meta.to_json(),
            "annotations": {},
            "layout": [[] for i in range(CNT_GRID_COLUMNS)],
        },
    }
    return CNT_GRID_COLUMNS, empty_gallery


# def preview(api: sly.Api, task_id, context, state, app_logger):
#     aug_info = get_aug_info(state)
#     aug = sly.imgaug_utils.build(aug_info)
#     preview_augs(api, task_id, aug, [aug_info])


def preview_pipeline(api: sly.Api, task_id, context, state, app_logger):
    random_order = False
    if len(pipeline) > 1:
        random_order = state["randomOrder"]
    augs = sly.imgaug_utils.build_pipeline(pipeline, random_order)
    py_code = sly.imgaug_utils.pipeline_to_python(pipeline, random_order)
    preview_augs(api, task_id, augs, pipeline, py_code)


def load_existing_pipeline(api: sly.Api, task_id, context, state, app_logger):
    remote_path = state["pipelinePath"]
    local_path = os.path.join(app.data_dir, sly.fs.get_file_name_with_ext(remote_path))
    api.file.download(team_id, remote_path, local_path)
    config = sly.json.load_json_file(local_path)
    _ = sly.imgaug_utils.build_pipeline(config["pipeline"], config["random_order"])  # validate
    global pipeline
    pipeline = config["pipeline"]

    fields = [
        {"field": "data.pipeline", "payload": config["pipeline"]},
        {"field": "state.addMode", "payload": False},
        {"field": "state.previewPy", "payload": None},
        {"field": "state.randomOrder", "payload": config["random_order"]},
    ]
    api.task.set_fields(task_id, fields)


def export_pipeline(api: sly.Api, task_id, context, state, app_logger):
    api.task.set_field(task_id, "state.exporting", True)

    random_order = False
    if len(pipeline) > 1:
        random_order = state["randomOrder"]

    name = state["saveName"]
    py_code = sly.imgaug_utils.pipeline_to_python(pipeline, random_order)
    py_path = os.path.join(app.data_dir, f"{name}.py")
    with open(py_path, "w") as text_file:
        text_file.writelines(py_code)

    json_path = os.path.join(app.data_dir, f"{name}.json")
    res_json = {"pipeline": pipeline, "random_order": random_order}
    sly.json.dump_json_file(res_json, json_path)

    remote_py_path = os.path.join(state["saveDir"], f"{name}.py")
    remote_json_path = os.path.join(state["saveDir"], f"{name}.json")

    if api.file.exists(team_id, remote_py_path):
        remote_py_path = api.file.get_free_name(team_id, remote_py_path)
    if api.file.exists(team_id, remote_json_path):
        remote_json_path = api.file.get_free_name(team_id, remote_json_path)

    infos = api.file.upload_bulk(team_id, [py_path, json_path], [remote_py_path, remote_json_path])
    fields = [
        {"field": "state.exporting", "payload": False},
        {"field": "state.savedUrl", "payload": api.file.get_url(infos[1].id)},
        {"field": "state.savedPath", "payload": infos[1].path},
    ]
    api.task.set_fields(task_id, fields)

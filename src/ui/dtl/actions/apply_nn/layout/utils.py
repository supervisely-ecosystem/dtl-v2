from typing import List
from supervisely import ProjectMeta
from supervisely.nn.inference.session import Session, SessionJSON

from src.ui.dtl.actions.apply_nn.layout.connect_model import *
from src.ui.dtl.actions.apply_nn.layout.select_classes import *
from src.ui.dtl.actions.apply_nn.layout.select_tags import *
from src.ui.dtl.actions.apply_nn.layout.node_layout import *

from src.ui.dtl.utils import (
    set_classes_list_preview,
    set_tags_list_preview,
)
import src.globals as g


### CONNECT MODEL AND MODEL INFO
def update_model_info_preview(session_id):
    connect_nn_model_info_empty_text.loading = True
    try:
        connect_nn_model_info.loading = True
        connect_nn_model_info.set_session_id(session_id)
    except:
        connect_nn_model_info_empty_text.set(
            "Couldn't connect to model. Check deployed model logs", status="error"
        )
        connect_nn_model_info.loading = False
        connect_nn_model_info_empty_text.loading = False
        return
    connect_nn_model_info.loading = False
    connect_nn_model_info_empty_text.loading = False
    connect_nn_model_info_empty_text.hide()


def connect_to_model(session_id: int, current_meta: ProjectMeta, model_info: ProjectMeta):
    update_preview_btn.disable()

    match_obj_classes_widget.hide()
    match_tag_metas_widget.hide()

    session_id = connect_nn_model_info._session_id
    if session_id is None:
        return

    try:
        session = Session(g.api, session_id)
        model_meta = session.get_model_meta()

        session_json = SessionJSON(g.api, session_id)
        model_info = session_json.get_session_info()
    except:
        raise ConnectionError("Couldn't connect to model. Check deployed model logs")

    model_name = model_info["app_name"]
    connect_nn_model_preview.set(model_name, "text")

    has_classes_conflict = check_conflict_classes(current_meta, model_meta)
    has_tags_conflict = check_conflict_tags(current_meta, model_meta)

    if not has_classes_conflict and not has_tags_conflict:
        update_preview_btn.enable()
        g.updater("metas")
    return current_meta, model_meta


def get_model_settings(session_id: int) -> tuple:
    try:
        session = Session(g.api, session_id)
        model_meta = session.get_model_meta()
        session_json = SessionJSON(g.api, session_id)
        model_info = session_json.get_session_info()
        model_settings = session.get_default_inference_settings()
    except:
        raise ConnectionError("Couldn't connect to model. Check deployed model logs")
    return model_meta, model_info, model_settings


def set_model_preview(model_info: dict) -> None:
    model_name = model_info["app_name"]
    connect_nn_model_preview.set(model_name, "text")


def set_model_settings(model_settings: dict) -> None:
    inf_settings_editor.loading = True
    model_settings_lines = [f"{key}: {value}" for key, value in model_settings.items()]
    inf_settings_editor.set_text("\n".join(model_settings_lines))
    inf_settings_editor.readonly = False
    inf_settings_editor.loading = False


### -----------------------------


### CLASSES AND TAGS
def set_model_classes(model_meta: ProjectMeta):
    classes_list_widget.loading = True
    obj_classes = [obj_class for obj_class in model_meta.obj_classes]

    classes_list_widget.set(obj_classes)
    classes_list_widget.select_all()

    saved_classes_settings = [obj_class.name for obj_class in model_meta.obj_classes]
    classes_list_widget.loading = False
    return saved_classes_settings


def set_model_classes_preview(saved_classes_settings: List[str]):
    set_classes_list_preview(classes_list_widget, classes_list_preview, saved_classes_settings)


def set_model_tags(model_meta: ProjectMeta):
    tags_list_widget.loading = True
    tag_metas = [tag_meta for tag_meta in model_meta.tag_metas]

    tags_list_widget.set(tag_metas)
    tags_list_widget.select_all()

    saved_tags_settings = [tag_meta.name for tag_meta in tag_metas]
    tags_list_widget.loading = False
    return saved_tags_settings


def set_model_tags_preview(saved_tags_settings: List[str]):
    set_tags_list_preview(tags_list_widget, tags_list_preview, saved_tags_settings)


### -----------------------------


### CHECK CURRENT AND MODEL META CONFLICTS | WON'T USE
def check_conflict_classes(current_meta: ProjectMeta, model_meta: ProjectMeta) -> bool:
    match_obj_classes_widget.hide()
    classes_list_widget.hide()
    has_classes_conflict = False
    original_classes = []
    conflict_classes = []
    for curr_obj_class in current_meta.obj_classes:
        model_obj_class = model_meta.get_obj_class(curr_obj_class.name)
        if model_obj_class is not None:
            if curr_obj_class.geometry_type != model_obj_class.geometry_type:
                original_classes.append(curr_obj_class)
                conflict_classes.append(model_obj_class)
    if len(conflict_classes) > 0:
        has_classes_conflict = True
        match_obj_classes_widget.set(original_classes, conflict_classes)
        classes_list_widget_notification.set(
            title="Classes conflict",
            description="Project meta and model meta have classes with the same names, but different shapes. Disable conflicting classes in previous nodes or select other model.",
        )
        match_obj_classes_widget.show()
    else:
        classes_list_widget_notification.set(
            title="No classes",
            description="Connect to deployed model to display classes.",
        )
        if len(model_meta.obj_classes) == 0:
            classes_list_widget_notification.show()
    if not has_classes_conflict:
        classes_list_widget.show()
    if len(model_meta.obj_classes) > 0 and not has_classes_conflict:
        set_model_classes(model_meta)
    else:
        set_model_classes(ProjectMeta())
    return has_classes_conflict


def check_conflict_tags(current_meta: ProjectMeta, model_meta: ProjectMeta) -> bool:
    tags_list_widget_notification.hide()
    tags_list_widget.hide()
    has_tags_conflict = False
    original_tags = []
    conflict_tags = []
    for curr_tag_meta in current_meta.tag_metas:
        model_tag_meta = model_meta.get_tag_meta(curr_tag_meta.name)
        if model_tag_meta is not None:
            original_tags.append(curr_tag_meta)
            conflict_tags.append(model_tag_meta)
    if len(conflict_tags) > 0:
        match_tag_metas_widget.set(original_tags, conflict_tags)
        conflict_stat = match_tag_metas_widget.get_stat()
        if (
            conflict_stat["different_value_type"] > 0
            or conflict_stat["different_one_of_options"] > 0
            or conflict_stat["different_value_type_suffix"] > 0
            or conflict_stat["different_one_of_options_suffix"] > 0
        ):
            has_tags_conflict = True
            tags_list_widget_notification.set(
                title="Tags conflict",
                description="Project meta and model meta have tag metas with the same names, but different values. Disable conflicting tags in previous nodes or select other model.",
            )
    if len(model_meta.tag_metas) == 0:
        tags_list_widget_notification.set(
            title="No tags",
            description="Connect to deployed model to display tags.",
        )
    if not has_tags_conflict:
        tags_list_widget_notification.show()
        tags_list_widget.show()
    else:
        match_tag_metas_widget.show()
        tags_list_widget.hide()
    if len(model_meta.tag_metas) > 0 and not has_tags_conflict:
        set_model_tags(model_meta)
    else:
        set_model_tags(ProjectMeta())
    return has_tags_conflict


### -----------------------------


### OTHER


def show_node_gui():
    connect_nn_model_preview.show()
    classes_list_edit_container.show()
    classes_list_preview.show()
    tags_list_edit_container.show()
    tags_list_preview.show()
    inf_settings_edit_container.show()


### -----------------------------

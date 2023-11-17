import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import Button
from supervisely import ProjectMeta
from supervisely.nn.inference import Session, SessionJSON
from supervisely import TagMeta, ObjClass
from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_classes_list_value,
    get_tags_list_value,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    get_layer_docs,
    set_tags_list_settings_from_json,
)
import src.globals as g

from src.ui.dtl.actions.apply_nn.layout.connect_model import *
from src.ui.dtl.actions.apply_nn.layout.select_classes import *
from src.ui.dtl.actions.apply_nn.layout.select_tags import *
from src.ui.dtl.actions.apply_nn.layout.apply_method import *
from src.ui.dtl.actions.apply_nn.layout.node_layout import *
from src.ui.dtl.actions.apply_nn.layout.utils import *


class ApplyNNAction(NeuralNetworkAction):
    name = "apply_nn"
    title = "Apply NN"
    docs_url = ""
    description = "Connect to deployed model and select apply options."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        _model_meta = ProjectMeta()
        _model_info = {}

        ### CONNECT TO MODEL BUTTONS
        @connect_nn_model_selector.value_changed
        def select_model_session(session_id):
            if session_id is None:
                return
            update_model_info_preview(session_id)

        @connect_nn_save_btn.click
        def confirm_model():
            nonlocal _current_meta, _model_meta, _model_info
            nonlocal saved_classes_settings, saved_tags_settings

            update_preview_btn.disable()
            match_obj_classes_widget.hide()
            match_tag_metas_widget.hide()

            session_id = connect_nn_model_info._session_id
            if session_id is None:
                return

            _model_meta, _model_info = get_model_settings(session_id)
            set_model_preview(_model_info)

            saved_classes_settings = set_model_classes(_model_meta)
            set_model_classes_preview(saved_classes_settings)

            saved_tags_settings = set_model_tags(_model_meta)
            set_model_tags_preview(saved_tags_settings)

            has_classes_conflict = check_conflict_classes(_current_meta, _model_meta)
            has_tags_conflict = check_conflict_tags(_current_meta, _model_meta)

            if not has_classes_conflict and not has_tags_conflict:
                update_preview_btn.enable()
                g.updater("metas")

        ### -----------------------

        saved_classes_settings = "default"
        default_classes_settings = "default"

        saved_tags_settings = "default"
        default_tags_settings = "default"

        def _get_classes_list_value():
            return get_classes_list_value(classes_list_widget, multiple=True)

        def _get_tags_list_value():
            return get_tags_list_value(tags_list_widget, multiple=True)

        def _save_classes_list_settings():
            nonlocal saved_classes_settings
            saved_classes_settings = _get_classes_list_value()

        def _save_tags_list_settings():
            nonlocal saved_tags_settings
            saved_tags_settings = _get_tags_list_value()

        def _set_default_classes_list_setting():
            # save setting to var
            nonlocal saved_classes_settings
            saved_classes_settings = copy.deepcopy(default_classes_settings)

        def _set_default_tags_list_setting():
            # save setting to var
            nonlocal saved_tags_settings
            saved_tags_settings = copy.deepcopy(default_tags_settings)

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta, _model_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            if connect_nn_model_info.session_id is None:
                return

            classes_list_widget.loading = True
            tags_list_widget.loading = True

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = [obj_class.name for obj_class in project_meta.obj_classes]
            has_classes_conflicts = check_conflict_classes(_current_meta, _model_meta)

            nonlocal saved_tags_settings
            saved_tags_settings = [tag_meta.name for tag_meta in project_meta.tag_metas]
            has_tags_conflicts = check_conflict_tags(_current_meta, _model_meta)

            classes_list_widget.loading = False
            tags_list_widget.loading = False

            if has_classes_conflicts or has_tags_conflicts:
                update_preview_btn.disable()
            else:
                update_preview_btn.enable()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            nonlocal saved_classes_settings, saved_tags_settings
            nonlocal _model_meta, _model_info

            apply_method = apply_nn_methods_selector.get_value()
            selected_model_classes = unpack_selected_model_classes(
                saved_classes_settings, _model_meta
            )
            selected_model_tags = unpack_selected_model_tags(saved_tags_settings, _model_meta)
            settings = {
                "session_id": connect_nn_model_info._session_id,
                "model_info": _model_info,
                "classes": selected_model_classes,
                "tags": selected_model_tags,
                "apply_method": apply_method,
            }
            return settings

        def _set_settings_from_json(settings: dict):
            apply_method = settings.get("type", "image")
            apply_nn_methods_selector.set_value(apply_method)

            # classes
            classes_list_widget.loading = True
            classes_list_settings = settings.get("classes", [])
            set_classes_list_settings_from_json(classes_list_widget, classes_list_settings)
            # save settings
            _save_classes_list_settings()
            # update settings preview
            set_model_classes_preview(saved_classes_settings)
            classes_list_widget.loading = False
            # -----------------------

            # tags
            tags_list_widget.loading = True
            tags_list_settings = settings.get("tags", [])
            set_tags_list_settings_from_json(tags_list_widget, tags_list_settings)
            # save settings
            _save_tags_list_settings()
            # update settings preview
            set_tags_list_preview(tags_list_widget, tags_list_preview, tags_list_settings)
            tags_list_widget.loading = False
            # -----------------------

        @classes_list_save_btn.click
        def classes_list_save_btn_cb():
            _save_classes_list_settings()
            set_model_classes_preview(saved_classes_settings)
            g.updater("metas")

        @classes_list_set_default_btn.click
        def classes_list_set_default_btn_cb():
            _set_default_classes_list_setting()
            set_classes_list_settings_from_json(classes_list_widget, saved_classes_settings)
            set_model_classes_preview(saved_classes_settings)
            g.updater("metas")

        @tags_list_save_btn.click
        def tags_list_save_btn_cb():
            _save_tags_list_settings()
            set_tags_list_preview(tags_list_widget, tags_list_preview, saved_tags_settings)
            g.updater("metas")

        @tags_list_set_default_btn.click
        def tags_list_set_default_btn_cb():
            _set_default_tags_list_setting()
            set_tags_list_settings_from_json(tags_list_widget, saved_tags_settings)
            set_tags_list_preview(tags_list_widget, tags_list_preview, saved_tags_settings)
            g.updater("metas")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = create_layout()
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            meta_changed_cb=meta_changed_cb,
            custom_update_btn=update_preview_btn,
        )

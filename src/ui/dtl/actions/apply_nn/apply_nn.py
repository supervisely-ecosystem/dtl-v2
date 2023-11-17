import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta
from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_classes_list_value,
    get_tags_list_value,
    set_classes_list_settings_from_json,
    set_tags_list_settings_from_json,
    get_layer_docs,
)
import src.globals as g

from src.ui.dtl.actions.apply_nn.layout.connect_model import *
from src.ui.dtl.actions.apply_nn.layout.select_classes import *
from src.ui.dtl.actions.apply_nn.layout.select_tags import *
from src.ui.dtl.actions.apply_nn.layout.inference_settings import *

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
        _model_settings = {}

        ### CONNECT TO MODEL BUTTONS
        @connect_nn_model_selector.value_changed
        def select_model_session(session_id):
            if session_id is None:
                return
            update_model_info_preview(session_id)

        @connect_nn_save_btn.click
        def confirm_model():
            nonlocal _current_meta, _model_meta, _model_info, _model_settings
            nonlocal saved_classes_settings, saved_tags_settings

            connect_notification.loading = True
            update_preview_btn.disable()

            session_id = connect_nn_model_info._session_id
            if session_id is None:
                return

            _model_meta, _model_info, _model_settings = get_model_settings(session_id)
            set_model_preview(_model_info)
            set_model_settings(_model_settings)

            saved_classes_settings = set_model_classes(_model_meta)
            set_model_classes_preview(saved_classes_settings)

            saved_tags_settings = set_model_tags(_model_meta)
            set_model_tags_preview(saved_tags_settings)

            connect_notification.hide()
            connect_notification.loading = False

            show_node_gui()
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

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            nonlocal saved_classes_settings, saved_tags_settings
            nonlocal _model_meta, _model_info, _model_settings

            session_id = connect_nn_model_info._session_id
            apply_method = apply_nn_methods_selector.get_value()
            model_suffix = model_suffix_input.get_value()
            use_model_suffix = always_add_suffix_checkbox.is_checked()
            model_conflict_method = resolve_conflict_method_selector.get_value()

            settings = {
                "current_meta": _current_meta.to_json(),
                "session_id": session_id,
                "model_info": _model_info,
                "model_meta": _model_meta.to_json(),
                "model_settings": _model_settings,
                "model_suffix": model_suffix,
                "model_conflict": model_conflict_method,
                "use_model_suffix": use_model_suffix,
                "apply_method": apply_method,
                "classes": saved_classes_settings,
                "tags": saved_tags_settings,
            }
            return settings

        def _set_settings_from_json(settings: dict):
            apply_method = settings.get("type", "image")
            apply_nn_methods_selector.set_value(apply_method)
            # @TODO: set other settings
            # session_id
            # model_info
            # model_meta
            # model_settings
            # model_suffix
            # model_conflict
            # use_model_suffix

            # classes
            classes_list_widget.loading = True
            classes_list_settings = settings.get("classes", [])
            set_classes_list_settings_from_json(classes_list_widget, classes_list_settings)
            _save_classes_list_settings()
            set_model_classes_preview(saved_classes_settings)
            classes_list_widget.loading = False
            # -----------------------

            # tags
            tags_list_widget.loading = True
            tags_list_settings = settings.get("tags", [])
            set_tags_list_settings_from_json(tags_list_widget, tags_list_settings)
            _save_tags_list_settings()
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

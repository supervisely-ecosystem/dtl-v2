from typing import Optional
from os.path import realpath, dirname
import json

from supervisely import logger
from supervisely.app.widgets import NodesFlow, Checkbox
from supervisely.project.project_meta import ProjectMeta
from src.ui.dtl.utils import get_layer_docs
from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
import src.ui.dtl.actions.output.output_project.layout.new_project as new_project
import src.ui.dtl.actions.output.output_project.layout.existing_project as existing_project
import src.globals as g


class OutputProjectAction(OutputAction):
    name = "output_project"
    title = "Output Project"
    docs_url = ""
    description = "Save results of data transformations to existing project in current workspace."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        saved_settings = {}
        _saved_meta = None
        project_meta = None

        is_existing_project = Checkbox("Export to existing project")
        new_project_name_text, new_project_name_input, new_project_container = (
            new_project.create_new_project_widgets()
        )
        (
            # SIDEBAR
            dst_project_selector,
            dst_dataset_options_existing_dataset_selector,
            dst_dataset_options_new_dataset_input,
            dst_dataset_options_selector,
            sidebar_save_button,
            select_project_warning_checkbox,
            select_project_warning_container,
            sidebar_container,
            # LAYOUT
            select_project_container,
            # PREVIEW
            dst_project_preview,
            dst_project_preview_warning,
            dst_dataset_preview,
            dst_preview_container,
        ) = existing_project.create_existing_project_widgets()

        select_project_container.hide()

        # SIDEBAR CBs
        @dst_project_selector.value_changed
        def on_dst_project_selector_change(project_id):
            dst_dataset_options_existing_dataset_selector.set_project_id(project_id)

        @sidebar_save_button.click
        def on_save_btn_click():
            dst_project_preview.show()
            dst_dataset_preview.show()
            _save_settings()

        # SWITCH PROJECT MODE
        @is_existing_project.value_changed
        def on_switch_project_mode(is_checked):
            if is_checked:
                new_project_container.hide()
                selected_project_id = dst_project_selector.get_selected_id()
                if selected_project_id is None:
                    dst_preview_container.hide()
                    select_project_warning_container.hide(),
                else:
                    dst_preview_container.show()
                    select_project_warning_container.show(),
                select_project_container.show()
            else:
                select_project_container.hide()
                dst_preview_container.hide()
                select_project_warning_container.hide(),
                new_project_container.show()

        def _update_preview():
            if is_existing_project.is_checked():
                selected_project_id = dst_project_selector.get_selected_id()
                if selected_project_id is not None:
                    project_info = g.api.project.get_info_by_id(selected_project_id)
                    if project_info.workspace_id != g.WORKSPACE_ID:
                        dst_project_preview.hide()
                        dst_dataset_preview.hide()
                        dst_project_preview_warning.set(
                            text=(
                                f"Project '{project_info.name}' (ID: '{project_info.id}') "
                                f"does not exist in the current workspace (ID: '{g.WORKSPACE_ID}'). "
                                "Please select a project from the current workspace."
                            ),
                            status="error",
                        )
                        dst_project_preview_warning.show()
                    else:
                        dst_project_preview.set(project_info)
                        dst_project_preview_warning.hide()
                        dst_project_preview.show()
                        dst_dataset_preview.show()

                    dataset_option = dst_dataset_options_selector.get_value()
                    if dataset_option == "new":
                        dst_dataset_preview.set(
                            f"Dataset: {dst_dataset_options_new_dataset_input.get_value()}", "text"
                        )
                    elif dataset_option == "existing":
                        dataset_name = g.api.dataset.get_info_by_id(
                            dst_dataset_options_existing_dataset_selector.get_selected_id()
                        ).name
                        dst_dataset_preview.set(f"Dataset: {dataset_name}", "text")
                    else:
                        dst_dataset_preview.set(
                            "Dataset(s) will keep structure from input project", "text"
                        )
                    dst_preview_container.show()

        def get_settings(options_json: dict):
            nonlocal saved_settings
            return {
                **saved_settings,
                "is_existing_project": is_existing_project.is_checked(),
                "merge_different_meta": select_project_warning_checkbox.is_checked(),
            }

        def _set_settings_from_json(settings: dict):
            project_mode = settings.get("is_existing_project", False)
            if project_mode:
                is_existing_project.check()
                new_project_container.hide()
                dataset_option = settings.get("dataset_option", "new")
                dst_dataset_options_selector.set_value(dataset_option)
                if dataset_option == "new":
                    dataset_name = settings.get("dataset_name", "")
                    dst_dataset_options_new_dataset_input.set_value(dataset_name)
                elif dataset_option == "existing":
                    dataset_id = settings.get("dataset_id", None)
                    dst_dataset_options_existing_dataset_selector.set_dataset_id(dataset_id)
                else:
                    pass
            else:
                is_existing_project.uncheck()
                new_project_container.show()
                project_name = settings.get("project_name", None)
                if project_name is not None:
                    new_project_name_input.set_value(project_name)
                else:
                    new_project_name_input.set_value("")
            _save_settings()

        def data_changed_cb(**kwargs):
            nonlocal _saved_meta, project_meta
            nonlocal saved_settings

            project_meta = kwargs.get("project_meta", None)

            if _saved_meta is None or project_meta == _saved_meta:
                select_project_warning_container.hide()
            else:
                select_project_warning_container.show()

        def _save_settings():
            nonlocal saved_settings
            nonlocal _saved_meta

            if not is_existing_project.is_checked():
                settings = {
                    "project_name": new_project_name_input.get_value(),
                    "dataset_option": None,
                    "dataset_name": None,
                    "dataset_id": None,
                    "merge_different_meta": False,
                }
                saved_settings = settings
            else:
                settings = {"project_name": None}
                project_id = dst_project_selector.get_selected_id()
                dataset_options = dst_dataset_options_selector.get_value()
                if dataset_options == "new":
                    settings["dataset_option"] = "new"
                    settings["dataset_name"] = dst_dataset_options_new_dataset_input.get_value()
                elif dataset_options == "existing":
                    settings["dataset_option"] = "existing"
                    settings["dataset_id"] = (
                        dst_dataset_options_existing_dataset_selector.get_selected_id()
                    )
                else:
                    settings["dataset_option"] = "keep"

                if project_id:
                    _saved_meta = g.api.project.get_meta(project_id)
                    _saved_meta = ProjectMeta.from_json(_saved_meta)
                    g.updater("metas")
                else:
                    _saved_meta = None
                saved_settings = settings
                _update_preview()

        def get_dst(options_json: dict) -> dict:
            if is_existing_project.is_checked():
                project_id = dst_project_selector.get_selected_id()
                if project_id is None:
                    return []
                dst = [str(project_id)]
                return dst
            else:
                dst = new_project_name_input.get_value()
                if dst is None or dst == "":
                    return []
                if dst[0] == "[":
                    dst = json.loads(dst)
                else:
                    dst = [dst.strip("'\"")]
                return dst

        def postprocess_cb():
            if is_existing_project.is_checked():
                propject_id = dst_project_selector.get_selected_id()
                project_info = g.api.project.get_info_by_id(propject_id)
                dst_project_preview.set(project_info)

        def _set_preview_from_json(dst):
            if is_existing_project.is_checked():
                if isinstance(dst, list):
                    if len(dst) != 0:
                        project_id = int(dst[0])
                    else:
                        project_id = None
                else:
                    project_id = int(dst)
                try:
                    dst_project_selector.set_project_id(project_id)
                    dst_dataset_options_existing_dataset_selector.set_project_id(project_id)
                    if project_id:
                        _saved_meta = g.api.project.get_meta(project_id)
                        _saved_meta = ProjectMeta.from_json(_saved_meta)
                    _update_preview()
                    data_changed_cb(project_meta=project_meta)
                except:
                    logger.debug(
                        f"Project does not exist in current workspace. Project id: '{project_id}', workspace id: '{g.WORKSPACE_ID}'"
                    )
                    dst_project_selector.set_project_id(None)
                    dst_dataset_options_existing_dataset_selector.set_project_id(None)
                    dst_project_preview.hide()
                    dst_project_preview_warning.set(
                        text=(
                            f"Project (ID: '{project_id}') "
                            f"does not exist in the current workspace (ID: '{g.WORKSPACE_ID}'). "
                            "Please select a project from the current workspace."
                        ),
                        status="error",
                    )
                    dst_dataset_preview.hide()
                    select_project_container.show()
                    dst_project_preview_warning.show()
                    dst_preview_container.show()
                    # _update_preview()

        def create_options(src: list, dst: list, settings: dict) -> dict:
            nonlocal project_meta, _saved_meta
            _set_settings_from_json(settings)
            _set_preview_from_json(dst)

            settings_options = [
                NodesFlow.Node.Option(
                    name="Project Mode",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=is_existing_project,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="New Project",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=new_project_container,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Existing Project",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=select_project_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(sidebar_container),
                        sidebar_width=400,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Destination Preview",
                    option_component=NodesFlow.WidgetOptionComponent(dst_preview_container),
                ),
                NodesFlow.Node.Option(
                    name="Approve Checkbox",
                    option_component=NodesFlow.WidgetOptionComponent(
                        select_project_warning_container
                    ),
                ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            data_changed_cb=data_changed_cb,
            get_settings=get_settings,
            get_dst=get_dst,
            need_preview=False,
            postprocess_cb=postprocess_cb,
        )

    @classmethod
    def create_outputs(cls):
        return []

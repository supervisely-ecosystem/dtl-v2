from typing import List, Optional
import copy
import os
from pathlib import Path
import requests

from supervisely.app.content import StateJson
from supervisely.app.widgets import (
    NodesFlow,
    SelectDataset,
    Text,
    Button,
    Container,
    Flexbox,
    NotificationBox,
)
from supervisely import ProjectType, ProjectMeta, ObjClassCollection

import src.utils as utils
import src.globals as g
from src.ui.dtl import SourceAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets.classes_mapping import ClassesMapping
from src.ui.widgets.classes_mapping_preview import ClassesMappingPreview
from src.ui.dtl.utils import (
    get_classes_mapping_value,
    classes_mapping_settings_changed_meta,
    set_classes_mapping_preview,
    get_set_settings_container,
    get_set_settings_button_style,
    set_classes_mapping_settings_from_json,
)


class DataAction(SourceAction):
    name = "data"
    title = "Data"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/data-layers/data"
    description = "Data layer (data) is used to specify project and its datasets that will participate in data transformation process."
    md_description_url = (
        "https://raw.githubusercontent.com/supervisely/docs/master/data-manipulation/dtl/data.md"
    )
    md_description = requests.get(md_description_url).text

    @classmethod
    def create_inputs(self):
        return []

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        # Src widgets
        select_datasets = SelectDataset(
            multiselect=True,
            select_all_datasets=True,
            allowed_project_types=[ProjectType.IMAGES],
            compact=False,
        )
        select_datasets_btn = Button(
            text="SELECT",
            icon="zmdi zmdi-folder",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        src_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        src_preview_widget = Text("")
        src_widgets_container = Container(widgets=[select_datasets, src_save_btn])

        saved_src = []

        # fix team and workspace for SelectDataset widget
        StateJson()[select_datasets._project_selector._ws_selector._team_selector.widget_id][
            "teamId"
        ] = g.TEAM_ID
        StateJson()[select_datasets._project_selector._ws_selector.widget_id][
            "workspaceId"
        ] = g.WORKSPACE_ID
        select_datasets._project_selector._ws_selector.disable()
        StateJson().send_changes()

        # Settings widgets
        _current_meta = ProjectMeta()
        empty_src_notification = NotificationBox(
            title="No classes",
            description="Choose datasets and ensure that source project have classes.",
        )
        classes_mapping_widget = ClassesMapping(empty_notification=empty_src_notification)
        classes_mapping_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        classes_mapping_set_default_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        classes_mapping_preview = ClassesMappingPreview()
        classes_mapping_widgets_container = Container(
            widgets=[
                classes_mapping_widget,
                Flexbox(
                    widgets=[
                        classes_mapping_save_btn,
                        classes_mapping_set_default_btn,
                    ],
                    gap=355,
                ),
            ]
        )

        default_classes_mapping_settings = "default"
        saved_classes_mapping_settings = "default"

        def _set_src_preview():
            src_preview_text = "".join(f"<li>{src.replace('/', ' / ')}</li>" for src in saved_src)
            src_preview_text = (
                f'<ul style="margin: 1px; padding: 0px 0px 0px 18px">{src_preview_text}<ul>'
            )
            src_preview_widget.text = src_preview_text

        def _save_src():
            def read_src_from_widget():
                ids = select_datasets.get_selected_ids()
                if ids is None or len(ids) == 0 or ids[0] is None:
                    ids = []
                project_info = None
                dataset_names = []
                for id in ids:
                    dataset_info = utils.get_dataset_by_id(id=id)
                    if project_info is None:
                        project_info = utils.get_project_by_id(id=dataset_info.project_id)
                    dataset_names.append(dataset_info.name)
                if project_info is None:
                    return []
                if project_info.datasets_count == len(dataset_names):
                    return [f"{project_info.name}/*"]
                return [f"{project_info.name}/{name}" for name in dataset_names]

            nonlocal saved_src
            saved_src = read_src_from_widget()

        def _get_classes_mapping_value():
            return get_classes_mapping_value(
                classes_mapping_widget,
                default_action="keep",
                ignore_action="keep",
                other_allowed=True,
                default_allowed=True,
            )

        def _set_classes_mapping_preview():
            set_classes_mapping_preview(
                classes_mapping_widget,
                classes_mapping_preview,
                saved_classes_mapping_settings,
                default_action="copy",
                ignore_action="keep",
                missing_value="default",
            )

        def _save_classes_mapping_setting():
            # save setting to var
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = _get_classes_mapping_value()

        def _set_default_classes_mapping_setting():
            # save setting to var
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = copy.deepcopy(default_classes_mapping_settings)

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
            classes_mapping_widget.loading = True
            old_obj_classes = classes_mapping_widget.get_classes()

            # set classes to widget
            classes_mapping_widget.set(project_meta.obj_classes)

            # update settings according to new meta
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = classes_mapping_settings_changed_meta(
                saved_classes_mapping_settings,
                old_obj_classes,
                project_meta.obj_classes,
                default_action="keep",
                ignore_action="keep",
                new_value="default",
                other_allowed=True,
            )
            if saved_classes_mapping_settings == {}:
                saved_classes_mapping_settings = "default"

            # update settings preview
            _set_classes_mapping_preview()

            classes_mapping_widget.loading = False

        def get_src(options_json: dict) -> List[str]:
            return saved_src

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes_mapping": saved_classes_mapping_settings,
            }

        def _set_src_from_json(srcs: List[str]):
            nonlocal saved_src
            if len(srcs) == 0:
                # set empty src to widget
                StateJson()[select_datasets._project_selector.widget_id]["projectId"] = None
                StateJson()[select_datasets.widget_id]["datasets"] = []
                select_datasets._all_datasets_checkbox.uncheck()
                StateJson().send_changes()

                # set empty project meta
                project_meta = ProjectMeta()
            else:
                # get all datasets
                first_project_name = None
                datasets = []
                for src in srcs:
                    project_name, dataset_name = src.split("/")
                    if first_project_name is None:
                        first_project_name = project_name
                    elif first_project_name != project_name:
                        raise RuntimeError("All datasets should be from the same project")
                    project_info = utils.get_project_by_name(name=project_name)
                    if dataset_name == "*":
                        datasets.extend(utils.get_all_datasets(project_info.id))
                    else:
                        datasets.append(utils.get_dataset_by_name(dataset_name, project_info.id))

                # set datasets to widget
                StateJson()[select_datasets._project_selector.widget_id][
                    "projectId"
                ] = project_info.id
                StateJson()[select_datasets.widget_id]["datasets"] = [ds.id for ds in datasets]
                if len(datasets) == project_info.datasets_count:
                    select_datasets._all_datasets_checkbox.check()
                else:
                    select_datasets._all_datasets_checkbox.uncheck()
                StateJson().send_changes()

                # get project meta
                project_meta = utils.get_project_meta(project_info.id)

            # save src
            _save_src()
            # set src preview
            _set_src_preview()
            # update meta
            meta_changed_cb(project_meta)

        def _set_settings_from_json(settings: dict):
            # if settings is empty, set default
            if settings.get("classes_mapping", "default") == "default":
                classes_mapping_widget.set_default()
            else:
                set_classes_mapping_settings_from_json(
                    classes_mapping_widget,
                    settings["classes_mapping"],
                    missing_in_settings_action="ignore",
                    missing_in_meta_action="ignore",
                )

            # save settings
            _save_classes_mapping_setting()
            # update settings preview
            _set_classes_mapping_preview()

        @src_save_btn.click
        def src_save_btn_cb():
            _save_src()
            _set_src_preview()
            g.updater("metas")

        @classes_mapping_save_btn.click
        def classes_mapping_save_btn_cb():
            _save_classes_mapping_setting()
            _set_classes_mapping_preview()
            g.updater("metas")

        @classes_mapping_set_default_btn.click
        def classes_mapping_set_default_btn_cb():
            _set_default_classes_mapping_setting()
            set_classes_mapping_settings_from_json(
                classes_mapping_widget,
                saved_classes_mapping_settings,
                missing_in_settings_action="ignore",
                missing_in_meta_action="ignore",
            )
            _set_classes_mapping_preview()
            g.updater("metas")

        def create_options(src: List[str], dst: List[str], settings: dict) -> dict:
            _set_src_from_json(src)
            _set_settings_from_json(settings)

            src_options = [
                NodesFlow.Node.Option(
                    name="Select Datasets",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=get_set_settings_container(
                            Text("Select Datasets"), select_datasets_btn
                        ),
                        sidebar_component=NodesFlow.WidgetOptionComponent(src_widgets_container),
                        sidebar_width=300,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="src_preview",
                    option_component=NodesFlow.WidgetOptionComponent(src_preview_widget),
                ),
            ]
            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Classes Mapping",
                    option_component=NodesFlow.ButtonOptionComponent(
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_mapping_widgets_container
                        ),
                        sidebar_width=630,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="classes_mapping_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_mapping_preview),
                ),
            ]
            return {"src": src_options, "dst": [], "settings": settings_options}

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_src=get_src,
            get_settings=get_settings,
            meta_changed_cb=meta_changed_cb,
        )

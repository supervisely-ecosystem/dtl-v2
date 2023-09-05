import copy
import traceback
from typing import List, Optional

import src.utils as utils
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.content import StateJson
from supervisely.app.widgets import NodesFlow, SelectDataset
from supervisely import ProjectType, ProjectMeta
from src.ui.widgets.classes_mapping import ClassesMapping
import src.globals as g


class DataAction(Action):
    name = "data"
    title = "Data"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/data-layers/data"
    description = "Data layer (data) is used to specify project and its datasets that will participate in data transformation process."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes_mapping": None,
    }

    @classmethod
    def create_inputs(self):
        return []

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        select_datasets = SelectDataset(
            multiselect=True,
            select_all_datasets=True,
            allowed_project_types=[ProjectType.IMAGES],
            compact=False,
        )
        StateJson()[select_datasets._project_selector._ws_selector._team_selector.widget_id][
            "teamId"
        ] = g.TEAM_ID
        StateJson()[select_datasets._project_selector._ws_selector.widget_id][
            "workspaceId"
        ] = g.WORKSPACE_ID
        select_datasets._project_selector._ws_selector.disable()
        StateJson().send_changes()
        classes_mapping_widget = ClassesMapping()

        def _get_classes_mapping_value():
            classes = classes_mapping_widget.get_classes()
            mapping = classes_mapping_widget.get_mapping()
            default = [
                cls_name for cls_name, cls_values in mapping.items() if cls_values["default"]
            ]
            if len(default) == len(classes):
                return "default"
            ignore = [cls_name for cls_name, cls_values in mapping.items() if cls_values["ignore"]]
            values = {
                name: values["value"]
                for name, values in mapping.items()
                if not values["ignore"] and not values["default"]
            }
            if len(ignore) > 0:
                values["__other__"] = "__ignore__"
                values.update({name: "__default__" for name in default})
            elif len(default) > 0:
                values["__other__"] = "__default__"
            return values

        def meta_changed_cb(project_meta: ProjectMeta):
            classes_mapping_widget.loading = True
            classes_mapping_widget.set(project_meta.obj_classes)
            classes_mapping_widget.loading = False

        def get_src(options_json: dict) -> List[str]:
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

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes_mapping": _get_classes_mapping_value(),
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            # set sources
            srcs = json_data["src"]
            if type(srcs) is str:
                srcs = [srcs]
            all_datasets = []
            first_project_name = None
            select_all_datasets_flag = False
            for src in srcs:
                project_name, dataset_name = src.split("/")
                if first_project_name is None:
                    first_project_name = project_name
                elif first_project_name != project_name:
                    raise RuntimeError("All datasets should be from the same project")
                project_info = utils.get_project_by_name(name=project_name)
                if dataset_name == "*":
                    select_all_datasets_flag = True
                    datasets = utils.get_all_datasets(project_info.id)
                else:
                    datasets = [utils.get_dataset_by_name(dataset_name, project_info.id)]
                all_datasets.extend(datasets)

            workspace_info = utils.get_workspace_by_id(project_info.workspace_id)
            StateJson()[select_datasets._project_selector._ws_selector._team_selector.widget_id][
                "teamId"
            ] = workspace_info.team_id
            StateJson()[select_datasets._project_selector._ws_selector.widget_id][
                "workspaceId"
            ] = project_info.workspace_id
            StateJson()[select_datasets._project_selector.widget_id]["projectId"] = project_info.id
            StateJson()[select_datasets.widget_id]["datasets"] = [ds.id for ds in all_datasets]
            if select_all_datasets_flag:
                select_datasets._all_datasets_checkbox.check()
            else:
                select_datasets._all_datasets_checkbox.uncheck()
            StateJson().send_changes()

            # load meta before setting classes mapping
            meta_changed_cb(utils.get_project_meta(project_info.id))

            # set settings
            settings = json_data["settings"]
            if settings["classes_mapping"] == "default":
                classes_mapping_widget.set_default()
            else:
                classes_mapping = {}
                other_default = settings["classes_mapping"].get("__other__", None) == "__default__"
                for cls in classes_mapping_widget.get_classes():
                    if cls.name in settings["classes_mapping"]:
                        value = settings["classes_mapping"][cls.name]
                        if value == "__default__":
                            value = cls.name
                        if value == "__ignore__":
                            value = ""
                        classes_mapping[cls.name] = value
                    elif other_default:
                        classes_mapping[cls.name] = cls.name
                    else:
                        classes_mapping[cls.name] = ""
                classes_mapping_widget.set_mapping(classes_mapping)
            return node_state

        @select_datasets.value_changed
        def select_datasets_changed_cb(value):
            if value is None or len(value) == 0 or value[0] is None:
                return
            try:
                dataset_info = utils.get_dataset_by_id(id=value[0])
                project_info = utils.get_project_by_id(id=dataset_info.project_id)
                project_meta = utils.get_project_meta(project_id=project_info.id)
                meta_changed_cb(project_meta)
            except Exception:
                traceback.print_exc()

        options = [
            NodesFlow.Node.Option(
                name="source_text",
                option_component=NodesFlow.TextOptionComponent("Source"),
            ),
            NodesFlow.Node.Option(
                name="Select Datasets",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(select_datasets)
                ),
            ),
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="classes_mapping_text",
                option_component=NodesFlow.TextOptionComponent("Classes Mapping"),
            ),
            NodesFlow.Node.Option(
                name="Set Classes Mapping",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_mapping_widget)
                ),
            ),
        ]

        return Layer(
            action=cls,
            id=layer_id,
            options=options,
            get_src=get_src,
            get_dst=None,
            get_settings=get_settings,
            meta_changed_cb=meta_changed_cb,
            set_settings_from_json=set_settings_from_json,
        )

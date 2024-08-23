# This module contains the functions that are used to configure the input and output of the workflow for the current app.

import json
from os.path import join, dirname
from src.ui.tabs.configure import nodes_flow
import src.ui.utils as ui_utils
import src.utils as utils
import src.globals as g
from typing import Union, Optional, List
import supervisely as sly

from supervisely.api.file_api import FileInfo
from supervisely.api.project_api import ProjectInfo
from supervisely.api.labeling_job_api import LabelingJobInfo
from src.compute.layers import Layer


def workflow_input(api: sly.Api, id: Union[int, str]):
    api.app.workflow.add_input_project(int(id))
    sly.logger.debug(f"Workflow: Input project - {id}")


def workflow_output(
    api: sly.Api,
    project_layers: Optional[List[Layer]] = None,
    job_layers: Optional[List[Layer]] = None,
    file_infos: Optional[List[FileInfo]] = None,
    preset_file: Optional[str] = None,
):

    try:
        file_infos: Optional[List[FileInfo]]
        project_infos: List[ProjectInfo] = [layer.sly_project_info for layer in project_layers]
        job_infos: List[LabelingJobInfo] = [layer.created_labeling_jobs for layer in job_layers]

        if project_layers is not None:
            for layer in project_layers:
                for project_info in layer:
                    api.app.workflow.add_output_project(project_info.id)
                    sly.logger.debug(f"Workflow: Output project - {project_info.id}")
        if job_infos is not None:
            for layer in job_layers:
                for job_info in layer:
                    api.app.workflow.add_output_job(job_info.id)
                    sly.logger.debug(f"Workflow: Output job - {job_info.id}")
        if file_infos is not None:
            n = len(file_infos)
            if n == 0:
                sly.logger.debug("Workflow: No output files")
                return
            folder_path = dirname(file_infos[0].path)
            relation_settings = sly.WorkflowSettings(
                title=f"Project Archives ({n})",
                icon="archive",
                icon_color="#ff4c9e",
                icon_bg_color="#d9f7e4",
            )
            meta = sly.WorkflowMeta(relation_settings=relation_settings)
            api.app.workflow.add_output_folder(folder_path, meta=meta)
            sly.logger.debug(f"Workflow: Output file - {file_infos[0]}")
        if preset_file is not None:
            relation_settings = sly.WorkflowSettings(
                title=preset_file.name,
                icon="dashboard",
                icon_color="#33c94c",
                icon_bg_color="#d9f7e4",
                url=f"/files/{preset_file.id}/true/?teamId={preset_file.team_id}",
                url_title="Show Preset",
            )
            meta = sly.WorkflowMeta(relation_settings=relation_settings)
            api.app.workflow.add_output_file(preset_file, meta=meta)
            sly.logger.debug(f"Workflow: Preset file - {preset_file}")
    except Exception as e:
        sly.logger.debug(f"Failed to add output to the workflow: {repr(e)}")


def upload_workflow_preset():
    edges = nodes_flow.get_edges_json()
    nodes_state = nodes_flow.get_nodes_state_json()
    nodes_json = nodes_flow.get_nodes_json()

    # save node order position
    scene_location = []
    for idx, node_json in enumerate(nodes_json):
        scene_location.append({"order_idx": idx, "position": node_json["position"]})

    # Init layers data
    layers_ids = ui_utils.init_layers(nodes_state)
    all_layers_ids = layers_ids["all_layers_ids"]
    ui_utils.init_src(edges)

    dtl_json = [g.layers[layer_id].to_json() for layer_id in all_layers_ids]
    for idx, layer_json in enumerate(dtl_json):
        layer_json["scene_location"] = scene_location[idx]

    preset_name = f"workflow_preset_{g.WORKFLOW_ID}"
    dst_path = f"{g.OFFLINE_SESSION_PATH}/{preset_name}.json"

    src_path = join(g.WORKFLOW_DIR, "/preset.json")
    utils.create_workflow_dir()
    with open(src_path, "w") as f:
        json.dump(dtl_json, f, indent=4)

    file_info = g.api.file.upload(g.TEAM_ID, src_path, dst_path)
    g.WORKFLOW_ID += 1
    return file_info

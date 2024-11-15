# AutoStart ML Pipelines from preset file

import os

import supervisely as sly
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

agent_id = 452  # 359
app_slug = "supervisely-ecosystem/data-nodes"

# preset_path = "/data-nodes/presets/images/preset.json"
preset_path = "/data-nodes/presets/images/api_pipeline.json"

module_id = api.app.get_ecosystem_module_id(app_slug)
module_info = api.app.get_ecosystem_module_info(module_id)


params = {"modalityType": "images", "slyFile": preset_path}

# app_params = {
#     "agent_id": agent_id,
#     # "app_id": 0,
#     "module_id": module_id,
#     "workspace_id": workspace_id,
#     "description": "Start ML Pipelines from py",
#     "task_name": "ML Pipelines",
#     "params": {"autostart": False, **params},
#     "app_version": None,
#     "is_branch": False,
# }

app_params = {
    "agent_id": agent_id,
    # "app_id": 0,
    "module_id": module_id,
    "workspace_id": workspace_id,
    "description": "Start ML Pipelines from API",
    "task_name": "ML Pipelines",
    "params": {"autostart": False, **params},
    "app_version": "run-from-api",
    "is_branch": True,
}

session_info = api.app.start(**app_params)

# Run pipeline
is_ready = api.app.wait_until_ready_for_api_calls(session_info.task_id)
if is_ready:
    api.task.send_request(task_id=session_info.task_id, method="run_pipeline", data={})

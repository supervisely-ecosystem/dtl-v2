# AutoStart ML Pipelines from preset file

import os

import supervisely as sly
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

agent_id = 555  # <- replace with your agent_id
app_slug = "supervisely-ecosystem/data-nodes"

preset_path = "/data-nodes/presets/images/preset.json"  # <- replace with your preset path

module_id = api.app.get_ecosystem_module_id(app_slug)
module_info = api.app.get_ecosystem_module_info(module_id)


params = {"modalityType": "images", "slyFile": preset_path}

app_params = {
    "agent_id": agent_id,
    "module_id": module_id,
    "workspace_id": workspace_id,
    "description": "Start ML Pipelines from py",
    "task_name": "ML Pipelines",
    "params": {"autostart": False, **params},
    "app_version": None,
    "is_branch": False,
}

session_info = api.app.start(**app_params)

# Uncomment to run pipeline after starting
# is_ready = api.app.wait_until_ready_for_api_calls(session_info.task_id)
# if is_ready:
#     api.task.send_request(task_id=session_info.task_id, method="run_pipeline", data={})

# Use to check pipeline progress
# status = api.task.send_request(task_id=task_id, method="get_pipeline_status", data={})
# print(status)

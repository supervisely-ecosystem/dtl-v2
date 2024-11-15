# Example on how to send API requests to ML Pipelines app from a script
# Available endpoints:
# 1. run_pipeline - runs a pipeline with current layers on the canvas
# 2. get_pipeline_status - returns the status of the pipeline ("Pipeline status is 21/50")

import os

import supervisely as sly
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()

api: sly.Api = sly.Api.from_env()

task_id = 55555  # <- replace with your task_id

is_ready = api.app.wait_until_ready_for_api_calls(task_id)
if is_ready:
    api.task.send_request(task_id=task_id, method="run_pipeline", data={})

# Use to check pipeline progress
# status = api.task.send_request(task_id=task_id, method="get_pipeline_status", data={})
# print(status)

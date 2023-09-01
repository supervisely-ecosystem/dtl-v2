import os
from dotenv import load_dotenv

import supervisely as sly


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
DATA_DIR = "sly_task_data/data"
RESULTS_DIR = "sly_task_data/results"
PREVIEW_DIR = "sly_task_data/preview"
STATIC_DIR = "static"

api = sly.Api()

cache = {
    "workspace_info": {},
    "project_id": {},
    "project_info": {},
    "project_meta": {},
    "dataset_id": {},
    "dataset_info": {},
    "all_datasets": {},
}

layers_count = 0
layers = {}

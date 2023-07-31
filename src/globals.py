import os
from typing import List
from dotenv import load_dotenv

import supervisely as sly


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))


WORKSPACE_ID = sly.env.workspace_id()

api = sly.Api()

import os
from typing import Optional, List, NamedTuple
from os.path import realpath, dirname
from supervisely.app.widgets import (
    NodesFlow,
    Input,
    Text,
    Select,
    RadioTable,
    Button,
    Container,
    Field,
    RadioTabs,
)
import pandas as pd
from supervisely.io.json import load_json_file

# from supervisely.api.agent_api import AgentInfo
from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size
import src.globals as g
from src.ui.dtl.utils import (
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
)


COL_ID = "id".upper()
COL_NAME = "name".upper()

columns = [
    COL_ID,
    COL_NAME,
]

AGENT_STATUS_RUNNING_ICON = "<i class='zmdi zmdi-circle' style='color: rgb(19, 206, 102);'></i>"
AGENT_STATUS_WAITING_ICON = "<i class='zmdi zmdi-circle' style='color: rgb(225, 75, 15);'></i> "
AGENT_STATUS_OTHER_ICON = "<i class='zmdi zmdi-circle' style='color: rgb(225, 75, 15);'></i> "

models_dir = os.path.join("src", "ui", "dtl", "actions", "deploy_yolov8", "models")
det_models_data_path = os.path.join(models_dir, "det_models_data.json")
seg_models_data_path = os.path.join(models_dir, "seg_models_data.json")
pose_models_data_path = os.path.join(models_dir, "pose_models_data.json")
det_models_data = load_json_file(det_models_data_path)
seg_models_data = load_json_file(seg_models_data_path)
pose_models_data = load_json_file(pose_models_data_path)


def get_agent_table_rows(agents_list: List[NamedTuple]):
    lines = []
    for agent in agents_list:
        agent_id = agent.id
        agent_name = agent.name

        agent_status = agent.status
        if agent_status == "running":
            agent_status_icon = AGENT_STATUS_RUNNING_ICON
        elif agent_status == "waiting":
            agent_status_icon = AGENT_STATUS_WAITING_ICON
        else:
            agent_status_icon = AGENT_STATUS_OTHER_ICON

        # agent_name_with_status = f"<div>{agent_status_icon} {agent_name}</div>"

        lines.append(
            [
                agent_id,
                agent_name,
            ]
        )
    return lines


def get_pretrained_model_table_rows(table: RadioTable):
    models_table_columns = [key for key in det_models_data[0].keys()]
    models_table_subtitles = [None] * len(models_table_columns)
    models_table_rows = []
    for element in det_models_data:
        models_table_rows.append(list(element.values()))
    table.set_data(
        columns=models_table_columns,
        rows=models_table_rows,
        subtitles=models_table_subtitles,
    )


def create_model_selector_widgets():
    # SIDEBAR

    # CUSTOM MODEL OPTION
    model_selector_sidebar_custom_model_table = RadioTable(columns=[], rows=[])
    model_selector_sidebar_custom_model_table_field = Field(
        title="Select custom model",
        description="",
        content=model_selector_sidebar_custom_model_table,
    )
    # ------------------------------

    # PRETRAINED MODEL OPTION
    model_selector_sidebar_public_model_table = RadioTable(columns=[], rows=[])
    get_pretrained_model_table_rows(model_selector_sidebar_public_model_table)
    model_selector_sidebar_public_model_table_field = Field(
        title="Select public model",
        description="",
        content=model_selector_sidebar_public_model_table,
    )

    # ------------------------------

    model_selector_sidebar_model_type = RadioTabs(
        titles=["Custom models", "Pretrained public  models"],
        descriptions=["Models trained by you", "Models trained by YOLOV8 team"],
        contents=[
            model_selector_sidebar_custom_model_table_field,
            model_selector_sidebar_public_model_table_field,
        ],
    )

    model_selector_sidebar_save_btn = create_save_btn()
    model_selector_sidebar_container = Container(
        [
            model_selector_sidebar_model_type,
            model_selector_sidebar_save_btn,
        ]
    )
    # ------------------------------

    # PREVIEW
    # TODO: App thumbnail widget
    model_selector_preview = Text("Selected model:", status="text", font_size=get_text_font_size())
    # ------------------------------

    # LAYOUT
    model_selector_layout_edit_text = Text(
        "Select serving app", status="text", font_size=get_text_font_size()
    )
    model_selector_layout_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )

    model_selector_layout_container = get_set_settings_container(
        model_selector_layout_edit_text, model_selector_layout_edit_btn
    )
    # ------------------------------

    return (
        # sidebar
        model_selector_sidebar_custom_model_table,
        model_selector_sidebar_public_model_table,
        model_selector_sidebar_model_type,
        model_selector_sidebar_save_btn,
        model_selector_sidebar_container,
        # preview
        model_selector_preview,
        # layout
        model_selector_layout_container,
    )

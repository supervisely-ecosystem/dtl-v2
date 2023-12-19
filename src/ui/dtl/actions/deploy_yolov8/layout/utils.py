import os
import re
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


def set_model_selector_preview(
    model_selector_sidebar_custom_model_table: RadioTable,
    model_selector_sidebar_public_model_table: RadioTable,
    model_selector_sidebar_model_type: RadioTabs,
    model_selector_preview: Text,
):
    model_type = model_selector_sidebar_model_type.get_active_tab()
    if model_type == "Custom models":
        row = model_selector_sidebar_custom_model_table.get_selected_row()
    else:  # "public"
        row = model_selector_sidebar_public_model_table.get_selected_row()
    model_name = row[0]
    model_selector_preview.set(model_name, "text")


def set_agent_selector_preview(
    agent_selector_sidebar_table: RadioTable, agent_selector_preview: Text
):
    row = agent_selector_sidebar_table.get_selected_row()
    agent_name = row[1]
    agent_selector_preview.set(f"Selected model: {agent_name}", "text")

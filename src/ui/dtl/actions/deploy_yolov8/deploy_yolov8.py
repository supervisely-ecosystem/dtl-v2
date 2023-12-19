from typing import Optional
from os.path import realpath, dirname
from supervisely.app.widgets import NodesFlow, Input, Text

from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size

from src.ui.dtl.actions.deploy_yolov8.layout.model_selector import create_model_selector_widgets
from src.ui.dtl.actions.deploy_yolov8.layout.agent_selector import create_agent_selector_widgets
import src.ui.dtl.actions.deploy_yolov8.layout.utils as utils


class DeployYOLOV8Action(NeuralNetworkAction):
    name = "deploy_yolov8"
    title = "Deploy YoloV8"
    docs_url = ""
    description = "Deploy YoloV8 models."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        # MODEL SELECTOR
        (  # sidebar
            model_selector_sidebar_custom_model_table,
            model_selector_sidebar_public_model_table,
            model_selector_sidebar_model_type,
            model_selector_sidebar_save_btn,
            model_selector_sidebar_container,
            # preview
            model_selector_preview,
            # layout
            model_selector_layout_container,
        ) = create_model_selector_widgets()

        # MODEL SELECTOR CBs
        @model_selector_sidebar_custom_model_table.value_changed
        def model_selector_sidebar_custom_model_table_cb(row):
            pass

        @model_selector_sidebar_public_model_table.value_changed
        def model_selector_sidebar_public_model_table_cb(row):
            pass

        @model_selector_sidebar_model_type.value_changed
        def model_selector_sidebar_model_type_cb(row):
            pass

        @model_selector_sidebar_save_btn.click
        def model_selector_sidebar_save_btn_cb():
            utils.set_model_selector_preview(
                model_selector_sidebar_custom_model_table,
                model_selector_sidebar_public_model_table,
                model_selector_sidebar_model_type,
                model_selector_preview,
            )
            # save_settings()

        # -----------------------------

        # AGENT SELECTOR
        (  # sidebar
            agent_selector_sidebar_table,
            agent_selector_sidebar_field,
            agent_selector_sidebar_save_btn,
            agent_selector_sidebar_container,
            # preview
            agent_selector_preview,
            # layout
            agent_selector_layout_container,
        ) = create_agent_selector_widgets()

        # AGENT SELECTOR CBs
        @agent_selector_sidebar_table.value_changed
        def agent_selector_sidebar_table_cb(row):
            pass

        @agent_selector_sidebar_save_btn.click
        def agent_selector_sidebar_save_btn_cb():
            utils.set_agent_selector_preview(agent_selector_sidebar_table, agent_selector_preview)
            # save_settings()

        # -----------------------------

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {}

        def _set_settings_from_json(settings: dict):
            pass

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Agent Selector",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=agent_selector_layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            agent_selector_sidebar_container
                        ),
                        sidebar_width=420,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Agent Selector Preview",
                    option_component=NodesFlow.WidgetOptionComponent(agent_selector_preview),
                ),
                NodesFlow.Node.Option(
                    name="Model Selector",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=agent_selector_layout_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            model_selector_sidebar_container
                        ),
                        sidebar_width=420,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="Model Selector Preview",
                    option_component=NodesFlow.WidgetOptionComponent(model_selector_preview),
                ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=False,
        )

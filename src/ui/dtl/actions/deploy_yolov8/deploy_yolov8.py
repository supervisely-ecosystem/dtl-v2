from typing import Optional
from time import sleep
from os.path import realpath, dirname

from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_layer_docs,
)

from src.ui.dtl.actions.deploy_yolov8.layout.model_selector import create_model_selector_widgets
from src.ui.dtl.actions.deploy_yolov8.layout.agent_selector import create_agent_selector_widgets
from src.ui.dtl.actions.deploy_yolov8.layout.model_serve import create_model_serve_widgets
from src.ui.dtl.actions.deploy_yolov8.layout.node_layout import create_node_layout
import src.ui.dtl.actions.deploy_yolov8.layout.utils as utils
import src.globals as g


class DeployYOLOV8Action(NeuralNetworkAction):
    name = "deploy_yolov8"
    title = "Deploy YoloV8"
    docs_url = ""
    description = "Deploy YoloV8 models."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        saved_settings = {}
        session = None

        # AGENT SELECTOR
        (  # sidebar
            agent_selector_sidebar_selector,
            agent_selector_sidebar_selector_empty_message,
            agent_selector_sidebar_field,
            agent_selector_sidebar_device_selector,
            agent_selector_sidebar_device_selector_empty_message,
            agent_selector_sidebar_save_btn,
            agent_selector_sidebar_device_selector_field,
            agent_selector_sidebar_container,
            # preview
            agent_selector_preview,
            agent_selector_device_preview,
            agent_selector_preview_container,
            # layout
            agent_selector_layout_container,
        ) = create_agent_selector_widgets()

        # AGENT SELECTOR CBs
        @agent_selector_sidebar_selector.value_changed
        def agent_selector_sidebar_selector_cb(value):
            agent_selector_sidebar_device_selector.loading = True
            agent_info = g.api.agent.get_info_by_id(value)
            devices = utils.get_agent_devices(agent_info)
            agent_selector_sidebar_device_selector.set(devices)
            agent_selector_sidebar_device_selector.loading = False

        @agent_selector_sidebar_save_btn.click
        def agent_selector_sidebar_save_btn_cb():
            nonlocal saved_settings
            saved_settings = utils.save_agent_settings(
                saved_settings,
                agent_selector_sidebar_selector,
                agent_selector_sidebar_device_selector,
            )
            utils.set_agent_selector_preview(
                agent_selector_sidebar_selector, agent_selector_preview
            )
            utils.set_agent_selector_device_preview(
                agent_selector_sidebar_device_selector, agent_selector_device_preview
            )

        # -----------------------------

        # MODEL SELECTOR
        (
            # sidebar
            # custom options
            model_selector_sidebar_custom_model_table_detection,
            model_selector_sidebar_custom_model_table_segmentation,
            model_selector_sidebar_custom_model_table_pose_estimation,
            model_selector_sidebar_custom_model_input,
            model_selector_sidebar_custom_model_option_selector,
            model_selector_sidebar_task_type_selector_custom,
            # public options
            model_selector_sidebar_public_model_table_detection,
            model_selector_sidebar_public_model_table_segmentation,
            model_selector_sidebar_public_model_table_pose_estimation,
            model_selector_sidebar_task_type_selector_public,
            # sidebar
            model_selector_sidebar_model_type_tabs,
            model_selector_sidebar_save_btn,
            model_selector_sidebar_container,
            # preview
            model_selector_preview,
            # layout
            model_selector_layout_container,
            model_selector_stop_model_after_inference_checkbox,
        ) = create_model_selector_widgets()

        # MODEL SELECTOR CBs
        @model_selector_sidebar_save_btn.click
        def model_selector_sidebar_save_btn_cb():
            nonlocal saved_settings
            saved_settings = utils.save_model_settings(
                saved_settings,
                model_selector_sidebar_model_type_tabs,
                model_selector_sidebar_task_type_selector_public,
                model_selector_sidebar_public_model_table_detection,
                model_selector_sidebar_public_model_table_segmentation,
                model_selector_sidebar_public_model_table_pose_estimation,
                model_selector_sidebar_custom_model_option_selector,
                model_selector_sidebar_custom_model_input,
                model_selector_sidebar_task_type_selector_custom,
                model_selector_sidebar_custom_model_table_detection,
                model_selector_sidebar_custom_model_table_segmentation,
                model_selector_sidebar_custom_model_table_pose_estimation,
                model_selector_stop_model_after_inference_checkbox,
            )
            utils.set_model_selector_preview(
                saved_settings,
                model_selector_preview,
            )

        # -----------------------------

        (
            model_serve_preview,
            model_serve_btn,
            model_serve_layout_container,
        ) = create_model_serve_widgets()
        # RUN MODEL

        # RUN MODEL CBs
        @model_serve_btn.click
        def model_serve_btn_cb():
            nonlocal saved_settings, session

            # if model_serve_btn.text == "STOP":
            #     g.api.app.stop(session.task_id)
            #     model_serve_btn.text = "RUN"
            #     model_serve_btn.style = "primary"
            #     return

            utils.set_model_serve_preview("", model_serve_preview)

            # add validation
            agent_id = saved_settings["agent_id"]
            device = saved_settings["device"]
            model_type = saved_settings["model_type"]
            model_path = saved_settings["model_path"]
            model_name = saved_settings["model_name"]
            task_type = saved_settings["task_type"]

            if session is None:
                session = utils.start_app(g.api, g.WORKSPACE_ID, saved_settings)

            # wait for task to start not working
            task_started = g.api.task.get_status(session.task_id)
            while not task_started is g.api.task.Status.STARTED:
                sleep(5)
                utils.set_model_serve_preview("Starting...", model_serve_preview)
                task_started = g.api.task.get_status(session.task_id)

            try:
                task_started = g.api.task.get_status(session.task_id)
                utils.deploy_model(g.api, session.task_id, saved_settings)
                app_link_message = (
                    f"Model deployed "
                    f"- <a href='{g.api.server_address}{g.api.app.get_url(session.task_id)}'>open app</a>"
                )
                utils.set_model_serve_preview(app_link_message, model_serve_preview, "success")
                saved_settings = utils.save_model_serve_settings(saved_settings, session.task_id)
                _save_settings()
            except:
                utils.set_model_serve_preview(
                    "An error occured while starting the app", model_serve_preview, "warning"
                )

        # -----------------------------

        def _save_settings() -> dict:
            nonlocal saved_settings
            saved_settings = utils.save_settings(
                saved_settings,
                agent_selector_sidebar_selector,
                agent_selector_sidebar_device_selector,
                model_selector_sidebar_model_type_tabs,
                model_selector_sidebar_task_type_selector_public,
                model_selector_sidebar_public_model_table_detection,
                model_selector_sidebar_public_model_table_segmentation,
                model_selector_sidebar_public_model_table_pose_estimation,
                model_selector_sidebar_custom_model_option_selector,
                model_selector_sidebar_custom_model_input,
                model_selector_sidebar_task_type_selector_custom,
                model_selector_sidebar_custom_model_table_detection,
                model_selector_sidebar_custom_model_table_segmentation,
                model_selector_sidebar_custom_model_table_pose_estimation,
                model_selector_stop_model_after_inference_checkbox,
            )

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings: dict):
            pass

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = create_node_layout(
                agent_selector_layout_container,
                agent_selector_sidebar_container,
                agent_selector_preview_container,
                model_selector_layout_container,
                model_selector_sidebar_container,
                model_selector_preview,
                model_selector_stop_model_after_inference_checkbox,
                model_serve_layout_container,
            )
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

# coding: utf-8
from typing import Tuple, Union
from time import sleep
from supervisely import (
    Annotation,
    Label,
    Rectangle,
    ObjClass,
    VideoAnnotation,
    Frame,
    VideoFigure,
    VideoObject,
    FrameCollection,
    VideoObjectCollection,
    logger,
)

from supervisely.nn.inference.session import Session
from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor, VideoDescriptor
import src.globals as g


def wait_model_served(session: Session, wait_attemtps: int = 10, wait_delay_sec: int = 10):
    for _ in range(wait_attemtps):
        is_model_served = session.is_model_served()
        if is_model_served:
            return
        else:
            sleep(wait_delay_sec)
            logger.warning("Model is not served yet. Waiting for model to be served")


def check_model_served(session: Session):
    is_model_served = session.is_model_served()
    if not is_model_served:
        is_model_served = wait_model_served(session)
        if not is_model_served:
            raise ValueError(
                (
                    "Selected model is not served in 'Deploy YOLOv8' node. "
                    "Make sure model is served by visiting app session page. "
                    # "Press 'SERVE' button to deploy model or close 'Deploy YOLOv8' node to proceed. "
                )
            )


class DeployYOLOV8(Layer):
    action = "deploy_yolov8"

    layer_settings = layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": [
                    "session_id",
                    "agent_id",
                    "device",
                    "model_source",
                    "checkpoint_name",
                    "task_type",
                    "checkpoint_url",
                    "stop_model_session",
                ],
                "properties": {
                    "session_id": {"type": "integer"},
                    "agent_id": {"type": "integer"},
                    "device": {"type": "string"},
                    "model_source": {"type": "string"},
                    "task_type": {"type": "string"},
                    "checkpoint_name": {"type": "string"},
                    "checkpoint_url": {"oneOf": [{"type": "string"}, {"type": "null"}]},
                    "stop_model_session": {"type": "boolean"},
                },
            },
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def validate(self):
        settings = self.settings

        if settings.get("agent_id", None) is None:
            raise ValueError("Select agent in 'Deploy YOLOv8' node'")
        if settings.get("device", None) is None:
            raise ValueError("Select device in 'Deploy YOLOv8' node")
        if settings.get("model_source", None) is None:
            raise ValueError("Select model in 'Deploy YOLOv8' node")
        if settings.get("session_id", None) is None:
            raise ValueError(
                "Selected model is not served in 'Deploy YOLOv8' node. Press'SERVE' button to deploy model or close 'Deploy YOLOv8' node to proceed"
            )

        session = Session(g.api, settings["session_id"])
        check_model_served(session)
        return super().validate()

    def postprocess(self):
        if self.settings["stop_model_session"]:
            g.api.app.stop(self.settings["session_id"])

    def modifies_data(self):
        return False

    def process(
        self,
        data_el: Tuple[Union[ImageDescriptor, VideoDescriptor], Union[Annotation, VideoAnnotation]],
    ):
        item_desc, ann = data_el
        yield item_desc, ann

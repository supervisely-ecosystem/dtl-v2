# coding: utf-8

from typing import Tuple

from supervisely import VideoAnnotation, Frame, VideoObject, VideoFigure

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import VideoDescriptor


class FilterVideobyDuration(Layer):
    action = "filter_video_by_duration"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["duration_unit", "min_duration", "max_duration"],
                "properties": {
                    "duration_unit": {
                        "type": "string",
                        "enum": [
                            "frames",
                            "seconds",
                        ],
                    },
                    "filter_duration": {"type": "integer", "minimum": 0},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def process(self, data_el: Tuple[VideoDescriptor, VideoAnnotation]):
        vid_desc, ann = data_el
        ann: VideoAnnotation

        duration_unit = self.settings["duration_unit"]
        filter_duration = self.settings["filter_duration"]

        if not self.net.preview_mode:
            # by frames
            if ann.frames_count <= filter_duration:
                yield data_el + tuple([1])  # True
            else:
                yield data_el + tuple([0])

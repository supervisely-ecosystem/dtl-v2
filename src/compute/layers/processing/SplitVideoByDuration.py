# coding: utf-8

from os.path import join, splitext
from typing import Tuple

from supervisely import VideoAnnotation, Frame, VideoObject, VideoFigure, FrameCollection
from supervisely.api.video.video_api import VideoInfo
from supervisely import KeyIdMap
from src.utils import LegacyProjectItem

from src.compute.Layer import Layer
from src.compute.dtl_utils.item_descriptor import VideoDescriptor
from moviepy.video.io.VideoFileClip import VideoFileClip
from supervisely.io.fs import get_file_name, get_file_ext
import src.globals as g

# Split functions


def split_video_by_frames(video_path: str, segment_length_in_frames: int) -> tuple:
    video = VideoFileClip(video_path)
    fps = video.fps
    frame_duration = 1 / fps
    segment_duration = segment_length_in_frames * frame_duration

    total_duration = video.duration
    start = 0
    end = segment_duration
    index = 1
    output_paths = []
    output_filenames = []

    video_name = get_file_name(video_path)
    video_ext = get_file_ext(video_path)

    while start < total_duration:
        end = min(end, total_duration)
        output_filename = f"{video_name}_{index}{video_ext}"
        output_path = join(g.RESULTS_DIR, output_filename)

        subclip = video.subclip(start, end)
        subclip.write_videofile(output_path)

        output_paths.append(output_path)
        output_filenames.append(output_filename)

        start = end
        end += segment_duration
        index += 1

    return output_paths, output_filenames


def split_video_by_seconds(video_path: str, segment_length_in_seconds: int) -> tuple:
    """
    Splits a video into multiple segments based on the given segment length in seconds.

    :param video_path: Path to the video file.
    :param segment_length_in_seconds: Length of each segment in seconds.
    :return: Tuple containing lists of paths and filenames for the split video files.
    """
    # Load the video
    video = VideoFileClip(video_path)

    total_duration = video.duration
    start = 0
    end = segment_length_in_seconds
    index = 1
    output_paths = []
    output_filenames = []

    video_name = get_file_name(video_path)
    video_ext = get_file_ext(video_path)

    while start < total_duration:
        end = min(end, total_duration)  # Ensure the end does not exceed the video's total duration
        output_filename = f"{video_name}_{index}{video_ext}"
        output_path = join(g.RESULTS_DIR, output_filename)

        subclip = video.subclip(start, end)
        subclip.write_videofile(output_path)

        output_paths.append(output_path)
        output_filenames.append(output_filename)

        start = end
        end += segment_length_in_seconds
        index += 1

    return output_paths, output_filenames


def process_splits(
    vid_desc: VideoDescriptor,
    video_path: str,
    video_name: str,
    video_shape: tuple,
    frames_count: int,
):
    video_name, item_ext = splitext(video_name)
    vid_desc = VideoDescriptor(
        LegacyProjectItem(
            project_name=vid_desc.get_pr_name(),
            ds_name=vid_desc.get_ds_name(),
            item_name=video_name,
            item_info=None,
            ia_data={"item_ext": item_ext},
            item_path=video_path,
            ann_path="",
        ),
        False,
    )
    vid_desc.update_video(video_path)
    ann = VideoAnnotation(video_shape, frames_count)
    return vid_desc, ann


# -----------------


class SplitVideobyDuration(Layer):
    action = "split_video_by_duration"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["duration_unit", "duration_threshold"],
                "properties": {
                    "duration_unit": {
                        "type": "string",
                        "enum": [
                            "frames",
                            "seconds",
                        ],
                    },
                    "duration_threshold": {"type": "integer", "minimum": 0},
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
        duration_threshold = self.settings["duration_threshold"]
        video_info: VideoInfo = vid_desc.info.item_info

        if not self.net.preview_mode:
            if len(ann.objects) > 0:
                raise NotImplementedError("Splitting is not supported for labeled videos yet")

            video_shape = (video_info.frame_height, video_info.frame_width)
            video_frames_count = video_info.frames_count

            video_length = video_info.frames_to_timecodes[-1]
            if duration_unit == "frames":
                if duration_threshold >= video_frames_count:
                    # Frames count set for splitting, is more then video
                    yield (vid_desc, ann)
                else:
                    video_splits_paths, video_splits_names = split_video_by_frames(
                        vid_desc.item_data, duration_threshold
                    )

                    for video_path, video_name in zip(video_splits_paths, video_splits_names):
                        yield process_splits(
                            vid_desc, video_path, video_name, video_shape, video_frames_count
                        )

            else:
                if duration_threshold >= video_info.duration:
                    # Time set for splitting, is more then video
                    yield (vid_desc, ann)
                else:
                    video_splits_paths, video_splits_names = split_video_by_seconds(
                        vid_desc.item_data, duration_threshold
                    )

                    for video_path, video_name in zip(video_splits_paths, video_splits_names):
                        yield process_splits(
                            vid_desc, video_path, video_name, video_shape, video_frames_count
                        )

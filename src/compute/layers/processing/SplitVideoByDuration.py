# coding: utf-8

from os.path import join, splitext, basename
from typing import Tuple, List

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
def split_video(
    video_path: str, ann: VideoAnnotation, segment_length: int, by_frames: bool = True
) -> Tuple[List[str], List[str]]:
    video = VideoFileClip(video_path)
    output_paths = []
    output_filenames = []

    video_name = get_file_name(video_path)
    video_ext = get_file_ext(video_path)

    total_duration = video.duration
    start = 0
    index = 1

    if by_frames:
        fps = video.fps
        frame_duration = 1 / fps
        segment_duration = segment_length * frame_duration
    else:
        segment_duration = segment_length

    end = segment_duration

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

    ann_segments = []
    for start in range(0, ann.frames_count, segment_length):
        end = min(start + segment_length - 1, ann.frames_count - 1)
        ann_segments.append([start, end])

    annotations = []
    frames = list([frame for frame in ann.frames])
    start = 0
    end = segment_length - 1
    total = ann.frames_count

    for _ in range(len(output_paths)):
        frame_range = FrameCollection(frames[start:end])
        ann = VideoAnnotation(
            img_size=(video.h, video.w),
            frames_count=1,
            objects=ann.objects,
            frames=frame_range,
            tags=ann.tags,
        )
        annotations.append(ann)

        start += segment_length
        end += segment_length
        if end > total:
            end = total

    return output_paths, output_filenames, annotations


def process_splits(
    vid_desc: VideoDescriptor, video_path: str, video_name: str, ann: VideoAnnotation
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
            # if len(ann.objects) > 0:
            #     raise NotImplementedError("Splitting is not supported for labeled videos yet")

            video_shape = (video_info.frame_height, video_info.frame_width)
            video_frames_count = video_info.frames_count

            video_length = video_info.frames_to_timecodes[-1]
            if duration_unit == "frames":
                if duration_threshold >= video_frames_count:
                    # Frames count set for splitting, is more then video
                    yield (vid_desc, ann)
                else:
                    video_splits_paths, video_splits_names, annotations = split_video(
                        vid_desc.item_data, ann, duration_threshold
                    )

                    for video_path, video_name, ann in zip(
                        video_splits_paths, video_splits_names, annotations
                    ):
                        yield process_splits(vid_desc, video_path, video_name, ann)

            else:
                if duration_threshold >= video_info.duration:
                    # Time set for splitting, is more then video
                    yield (vid_desc, ann)
                else:
                    video_splits_paths, video_splits_names, annotations = split_video(
                        vid_desc.item_data, ann, duration_threshold, False
                    )

                    for video_path, video_name, ann in zip(
                        video_splits_paths, video_splits_names, annotations
                    ):
                        yield process_splits(vid_desc, video_path, video_name, ann)

        # annotation = VideoAnnotation(
        #     img_size=(video.h, video.w),
        #     frames_count=ann_segments[index - 1][1] + 1 - ann_segments[index - 1][0],
        #     objects=ann.objects,
        #     frames=FrameCollection(
        #         [frame for frame in frames[ann_segments[index - 1][0] : ann_segments[index - 1][1]]]
        #     ),
        #     tags=ann.tags,
        # )
        # annotations.append(annotation)

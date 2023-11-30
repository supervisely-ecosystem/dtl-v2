from typing import Union, Callable
from supervisely import (
    Annotation,
    VideoAnnotation,
    FrameCollection,
    ProjectMeta,
    Frame,
    VideoObject,
    VideoObjectCollection,
)


def apply_to_labels(ann: Union[Annotation, VideoAnnotation], fn: Callable):
    """fn must receive a single argument of type Label and return iterable of labels"""
    new_labels = []
    for label in ann.labels:
        new_labels.extend(fn(label))
    ann = ann.clone(labels=new_labels)
    return ann


def apply_to_frames(ann: VideoAnnotation, fn: Callable):
    """fn must receive a single argument of type Frame and return iterable of frames"""
    new_frames = []
    for frame in ann.frames:
        new_frames.extend(fn(frame))
    frames_col = FrameCollection(new_frames)
    ann = ann.clone(frames=frames_col)
    return ann

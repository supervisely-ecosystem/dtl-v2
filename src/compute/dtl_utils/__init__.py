from typing import Union, Callable
from supervisely import Annotation, VideoAnnotation, FrameCollection


def apply_to_labels(ann: Union[Annotation, VideoAnnotation], fn: Callable):
    """fn must receive a single argument of type Label and return iterable of labels"""

    if isinstance(ann, Annotation):
        new_labels = []
        for label in ann.labels:
            new_labels.extend(fn(label))
        ann = ann.clone(labels=new_labels)
        return ann

    if isinstance(ann, VideoAnnotation):
        new_frames = []
        for frame in ann.frames:
            new_frames.extend(fn(frame))
        frames_col = FrameCollection(new_frames)
        ann = ann.clone(frames=frames_col)
    return ann

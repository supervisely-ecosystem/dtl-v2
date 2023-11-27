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


def convert_video_annotation(ann: VideoAnnotation, dst_meta: ProjectMeta):
    frames = []
    new_objects = {}

    for curr_object in ann.objects:
        new_obj_class = dst_meta.obj_classes.get(curr_object.obj_class.name)
        if curr_object.obj_class.geometry_type == new_obj_class.geometry_type:
            new_objects[curr_object.key] = curr_object
        else:
            new_object = VideoObject(obj_class=new_obj_class, tags=curr_object.tags)
            new_objects[curr_object.key] = new_object

    for curr_frame in ann.frames:
        new_frame_figures = []
        for curr_figure in curr_frame.figures:
            curr_figure_obj_class = curr_figure.video_object.obj_class
            new_obj_class = dst_meta.obj_classes.get(curr_figure_obj_class.name)
            if curr_figure_obj_class.geometry_type == new_obj_class.geometry_type:
                new_frame_figures.append(curr_figure)
            else:
                new_geometries = curr_figure.geometry.convert(new_obj_class.geometry_type)
                for new_geometry in new_geometries:
                    new_figure = curr_figure.clone(
                        video_object=new_objects[curr_figure.video_object.key],
                        geometry=new_geometry,
                    )
                    new_frame_figures.append(new_figure)
        new_frame = Frame(curr_frame.index, new_frame_figures)
        frames.append(new_frame)

    new_frames_collection = FrameCollection(frames)
    new_objects = VideoObjectCollection(list(new_objects.values()))

    return ann.clone(objects=new_objects, frames=new_frames_collection)

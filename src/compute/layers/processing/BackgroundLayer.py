# coding: utf-8
from typing import Tuple, Union

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
)

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils.item_descriptor import ImageDescriptor, VideoDescriptor


def add_bg_to_image(ann: Annotation, bg_class: ObjClass, bg_geometry: Rectangle) -> Annotation:
    bg_label = Label(
        geometry=bg_geometry,
        obj_class=bg_class,
    )
    ann = ann.add_label(bg_label)
    return ann


def add_bg_to_video(
    ann: VideoAnnotation, bg_class: ObjClass, bg_geometry: Rectangle
) -> VideoAnnotation:
    frames = ann.frames
    bg_object = VideoObject(obj_class=bg_class)
    new_frames = []
    for frame in frames:
        bg_figure = VideoFigure(bg_object, bg_geometry, frame.index)
        frame_figures = frame.figures
        frame_figures.append(bg_figure)
        frame = frame.clone(frame.index, frame_figures)
        new_frames.append(frame)
    video_objects = ann.objects.add(bg_object)
    ann = ann.clone(
        frames=FrameCollection(new_frames), objects=VideoObjectCollection(video_objects)
    )
    return ann


class BackgroundLayer(Layer):
    action = "background"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["class"],
                "properties": {"class": {"type": "string"}},
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)
        self.src_check_mappings = [self.settings["class"]]

    def define_classes_mapping(self):
        self.cls_mapping[ClassConstants.NEW] = [
            {"title": self.settings["class"], "shape": Rectangle.geometry_name()}
        ]
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def modifies_data(self):
        return True

    def process(
        self,
        data_el: Tuple[Union[ImageDescriptor, VideoDescriptor], Union[Annotation, VideoAnnotation]],
    ):
        item_desc, ann = data_el

        h, w = ann.img_size
        bg_geometry = Rectangle(0, 0, h - 1, w - 1)
        bg_class = ObjClass(self.settings["class"], Rectangle)

        if isinstance(ann, Annotation):
            ann = add_bg_to_image(ann, bg_class, bg_geometry)
            yield item_desc, ann
        else:
            ann = add_bg_to_video(ann, bg_class, bg_geometry)
            yield item_desc, ann

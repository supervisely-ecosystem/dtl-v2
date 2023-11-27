# coding: utf-8

from supervisely import (
    Rectangle,
    Label,
    Annotation,
    VideoAnnotation,
    Frame,
    VideoObject,
    FrameCollection,
    VideoObjectCollection,
    ProjectMeta,
)

from src.compute.Layer import Layer
from src.compute.classes_utils import ClassConstants
from src.compute.dtl_utils import apply_to_labels


def convert_objects_to_bbox(ann: VideoAnnotation, dst_meta: ProjectMeta):
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


class BBoxLayer(Layer):
    action = "bbox"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["classes_mapping"],
                "properties": {
                    "classes_mapping": {
                        "type": "object",
                        "patternProperties": {".*": {"type": "string"}},
                    }
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def define_classes_mapping(self):
        for old_class, new_class in self.settings["classes_mapping"].items():
            self.cls_mapping[old_class] = {"title": new_class, "shape": Rectangle.geometry_name()}
        self.cls_mapping[ClassConstants.OTHER] = ClassConstants.DEFAULT

    def process(self, data_el):
        img_desc, ann = data_el

        def to_fig_rect(label: Label):
            new_title = self.settings["classes_mapping"].get(label.obj_class.name)
            if new_title is None:
                return [label]
            rect = label.geometry.to_bbox()
            new_obj_class = label.obj_class.clone(
                name=new_title, geometry_type=Rectangle
            )  # keep color?
            label = label.clone(
                geometry=rect, obj_class=new_obj_class
            )  # keep description and binding key?
            return [label]  # iterable

        if isinstance(ann, Annotation):
            ann = apply_to_labels(ann, to_fig_rect)
        else:
            ann = convert_objects_to_bbox(ann, self.output_meta)
        yield img_desc, ann

from typing import Optional, Union, List
from supervisely.app.widgets import Widget
from supervisely import ObjClass, ObjClassCollection
from supervisely.app import DataJson, StateJson

from supervisely.geometry.bitmap import Bitmap
from supervisely.geometry.cuboid import Cuboid
from supervisely.geometry.point import Point
from supervisely.geometry.polygon import Polygon
from supervisely.geometry.polyline import Polyline
from supervisely.geometry.rectangle import Rectangle
from supervisely.geometry.graph import GraphNodes
from supervisely.geometry.any_geometry import AnyGeometry
from supervisely.geometry.cuboid_3d import Cuboid3d
from supervisely.geometry.pointcloud import Pointcloud
from supervisely.geometry.point_3d import Point3d
from supervisely.geometry.multichannel_bitmap import MultichannelBitmap
from supervisely.geometry.closed_surface_mesh import ClosedSurfaceMesh


type_to_shape_text = {
    AnyGeometry: "any shape",
    Rectangle: "rectangle",
    Polygon: "polygon",
    Bitmap: "bitmap (mask)",
    Polyline: "polyline",
    Point: "point",
    Cuboid: "cuboid",  #
    Cuboid3d: "cuboid 3d",
    Pointcloud: "pointcloud",  #  # "zmdi zmdi-border-clear"
    MultichannelBitmap: "n-channel mask",  # "zmdi zmdi-collection-item"
    Point3d: "point 3d",  # "zmdi zmdi-select-all"
    GraphNodes: "keypoints",
    ClosedSurfaceMesh: "volume (3d mask)",
}


class ClassesMapping(Widget):
    def __init__(
        self,
        classes: Optional[Union[List[ObjClass], ObjClassCollection]] = [],
        widget_id: Optional[str] = None,
    ):
        self._classes = classes
        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {
            "classes": [
                {
                    **cls.to_json(),
                    "shape_text": type_to_shape_text.get(cls.geometry_type).upper(),
                    "default_value": cls.name,
                }
                for cls in self._classes
            ]
        }

    def get_json_state(self):
        return {
            "classes_values": [
                {
                    "value": cls.name,
                    "default": True,
                    "ignore": False,
                }
                for cls in self._classes
            ]
        }

    def set(self, classes):
        self._classes = classes
        self.update_data()
        DataJson().send_changes()
        cur_mapping = self.get_mapping()
        new_mapping_values = []
        for cls in self._classes:
            value = cur_mapping.get(
                cls.name,
                {
                    "value": cls.name,
                    "default": False,
                    "ignore": True,
                },
            )
            new_mapping_values.append(value)
        StateJson()[self.widget_id]["classes_values"] = new_mapping_values
        StateJson().send_changes()

    def get_classes(self):
        return self._classes

    def get_mapping(self):
        classes_values = StateJson()[self.widget_id]["classes_values"]
        if len(classes_values) != len(self._classes):
            self.update_state()
            return self.get_mapping()
        mapping = {cls.name: classes_values[idx] for idx, cls in enumerate(self._classes)}
        return mapping

    def ignore(self, indexes: List[int]):
        classes_values = StateJson()[self.widget_id]["classes_values"]
        for idx in indexes:
            classes_values[idx] = {"value": "", "default": False, "ignore": True}
        StateJson()[self.widget_id]["classes_values"] = classes_values
        StateJson().send_changes()

    def set_default(self):
        self.update_state()
        StateJson().send_changes()

    def set_mapping(self, mapping: dict):
        cur_mapping = self.get_mapping()
        new_mapping_values = []
        for cls in self._classes:
            cur_value = cur_mapping.get(cls.name, {"value": ""}).get("value")
            new_value = mapping.get(cls.name, cur_value)
            new_mapping_values.append(
                {
                    "value": new_value,
                    "default": new_value == cls.name,
                    "ignore": new_value == "",
                }
            )
        StateJson()[self.widget_id]["classes_values"] = new_mapping_values
        StateJson().send_changes()

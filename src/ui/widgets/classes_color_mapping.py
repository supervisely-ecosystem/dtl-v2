from typing import List
from supervisely.imaging.color import rgb2hex
from supervisely.app import StateJson, DataJson
from src.ui.widgets.classes_mapping.classes_mapping import (
    ClassesMapping,
    type_to_shape_text,
)


class ClassesColorMapping(ClassesMapping):
    def get_json_data(self):
        return {
            "classes": [
                {
                    **cls.to_json(),
                    "shape_text": type_to_shape_text.get(cls.geometry_type).upper(),
                    "default_value": rgb2hex(cls.color),
                }
                for cls in self._classes
            ]
        }

    def get_json_state(self):
        return {
            "classes_values": [
                {
                    "value": rgb2hex(cls.color),
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
                    "value": rgb2hex(cls.color),
                    "default": False,
                    "ignore": True,
                },
            )
            new_mapping_values.append(value)
        StateJson()[self.widget_id]["classes_values"] = new_mapping_values
        StateJson().send_changes()

    def set_colors(self, classes_colors: List[List[int]]):
        classes_values = StateJson()[self.widget_id]["classes_values"]
        for idx, cls in enumerate(self._classes):
            rgb_color = classes_colors[idx]
            classes_values[idx]["value"] = rgb2hex(rgb_color)
            classes_values[idx]["default"] = tuple(cls.color) == tuple(rgb_color)
            classes_values[idx]["ignore"] = False
        StateJson()[self.widget_id]["classes_values"] = classes_values
        StateJson().send_changes()

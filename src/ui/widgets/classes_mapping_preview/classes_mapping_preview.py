from typing import Optional, Union, List

from supervisely import ObjClass, ObjClassCollection
from supervisely.app import StateJson
from supervisely.app.widgets import Widget


class ClassesMappingPreview(Widget):
    def __init__(
        self,
        classes: Optional[Union[List[ObjClass], ObjClassCollection]] = [],
        mapping: Optional[dict] = {},
        max_height: str = "128px",
        widget_id: Optional[str] = None,
    ):
        self._classes = classes
        self._mapping = mapping
        self._max_height = max_height
        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {
            "max_height": self._max_height,
        }

    def get_json_state(self):
        return {
            "mapping": [
                {"class": cls.to_json(), "value": self._mapping.get(cls.name, "")}
                for cls in self._classes
            ]
        }

    def set(self, classes: Union[List[ObjClass], ObjClassCollection], mapping: dict):
        self._classes = classes
        self._mapping = mapping
        StateJson()[self.widget_id] = self.get_json_state()
        StateJson().send_changes()

    def set_mapping(self, mapping: dict):
        self._mapping = mapping
        StateJson()[self.widget_id] = self.get_json_state()
        StateJson().send_changes()

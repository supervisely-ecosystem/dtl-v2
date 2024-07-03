import os
from collections import OrderedDict
from typing import List
from supervisely.app.widgets import Widget
import supervisely as sly
from supervisely.io.json import load_json_file
from supervisely.app import StateJson, DataJson


class AugsList(Widget):
    class Routes:
        MOVE_AUG_UP = "move_aug_up_cb"
        MOVE_AUG_DOWN = "move_aug_down_cb"
        DELETE_AUG = "delete_aug_cb"

    class AugItem:
        def __init__(
            self, category: str, method: str, params: dict, sometimes: float = None
        ) -> None:
            self.category = category
            self.method = method
            self.params = params
            self.sometimes = sometimes

            # self.default_py = AugsList._augs_config[category][method]["py"]
            self.python = self._generate_py()

        def _generate_py(self):
            py = (
                f"iaa.{self.method}({''.join([f'{k}={v}, ' for k, v in self.params.items()])[:-2]})"
            )
            if self.sometimes is not None:
                py = f"iaa.Sometimes({self.sometimes}, {py})"
            return py

        def get_py(self):
            return self.python

        def to_json(self):
            return {
                "category": self.category,
                "method": self.method,
                "params": self.params,
                "sometimes": self.sometimes,
                "python": self.python,
            }

    def __init__(self, pipeline: List[AugItem] = [], shuffle: bool = False, widget_id: str = None):
        self._pipeline = pipeline
        # self._augs_config = load_json_file(os.path.join(os.path.dirname(__file__), "augs.json"))
        self._shuffle = shuffle
        self._py_options = {
            "mode": "ace/mode/python",
            "showGutter": False,
            "readOnly": True,
            "maxLines": 1,
            "highlightActiveLine": False,
        }

        self._delete_aug_clicked = False
        self._move_aug_up_clicked = False
        self._move_aug_down_clicked = False
        self._pipeline_json = [aug.get_py() for aug in self._pipeline]
        super().__init__(widget_id=widget_id, file_path=__file__)

        server = self._sly_app.get_server()

        # DELETE_AUG
        del_route_path = self.get_route_path(AugsList.Routes.DELETE_AUG)

        @server.post(del_route_path)
        def _click():
            index = StateJson()[self.widget_id]["augIndex"]
            if index is not None:
                del self._pipeline[index]
            self._pipeline_json = [aug.get_py() for aug in self._pipeline]
            DataJson()[self.widget_id]["pipeline"] = self._pipeline_json
            DataJson().send_changes()
            StateJson()[self.widget_id]["augIndex"] = None
            StateJson().send_changes()

        # MOVE_AUG_UP
        mv_up_route_path = self.get_route_path(AugsList.Routes.MOVE_AUG_UP)

        @server.post(mv_up_route_path)
        def _click():
            index = StateJson()[self.widget_id]["augIndex"]
            if index is not None and index > 0:
                a = self._pipeline[index - 1]
                self._pipeline[index - 1] = self._pipeline[index]
                self._pipeline[index] = a
            self._pipeline_json = [aug.get_py() for aug in self._pipeline]
            DataJson()[self.widget_id]["pipeline"] = self._pipeline_json
            DataJson().send_changes()
            StateJson()[self.widget_id]["augIndex"] = None
            StateJson().send_changes()
            return

        # MOVE_AUG_DOWN
        mv_down_route_path = self.get_route_path(AugsList.Routes.MOVE_AUG_DOWN)

        @server.post(mv_down_route_path)
        def _click():
            index = StateJson()[self.widget_id]["augIndex"]
            if index is not None and index < len(self._pipeline) - 1:
                a = self._pipeline[index + 1]
                self._pipeline[index + 1] = self._pipeline[index]
                self._pipeline[index] = a
            self._pipeline_json = [aug.get_py() for aug in self._pipeline]
            DataJson()[self.widget_id]["pipeline"] = self._pipeline_json
            DataJson().send_changes()
            StateJson()[self.widget_id]["augIndex"] = None
            StateJson().send_changes()
            return

    def get_json_data(self):
        return {
            "pipeline": self._pipeline_json,
        }

    def get_json_state(self):
        return {
            "shuffle": self._shuffle,
            "options": self._py_options,
            "augIndex": None,
        }

    def get_pipeline(self):
        return self._pipeline

    def set_pipeline(self, pipeline):
        self._pipeline = pipeline
        self._pipeline_json = [aug.get_py() for aug in self._pipeline]
        DataJson()[self.widget_id]["pipeline"] = self._pipeline_json
        DataJson().send_changes()

    def append_aug(self, category: str, method: str, params: dict, sometimes: float = None):
        aug = AugsList.AugItem(category, method, params, sometimes)
        self._pipeline.append(aug)
        self._pipeline_json = [aug.get_py() for aug in self._pipeline]
        DataJson()[self.widget_id]["pipeline"] = self._pipeline_json
        DataJson().send_changes()

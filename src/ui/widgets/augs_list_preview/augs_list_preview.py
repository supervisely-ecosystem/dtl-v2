from typing import List, Dict
from supervisely.app.widgets import Widget
from supervisely.app import StateJson, DataJson

aug_icon_map = {
    "arithmetic": "zmdi zmdi-plus-1",
    "blur": "zmdi zmdi-blur",
    "color": "zmdi zmdi-palette",
    "contrast": "zmdi zmdi-brightness-4",
    "convolution": "zmdi zmdi-memory",
    "flip": "zmdi zmdi-flip-to-front",
    "geometric": "zmdi zmdi-shape",
    "imgcorruptlike": "zmdi zmdi-broken-image",
    "pillike": "zmdi zmdi-format-valign-center",
    "segmentation": "zmdi zmdi-male-alt",
    "size": "zmdi zmdi-photo-size-select-large",
}


class AugsListPreview(Widget):

    def __init__(
        self,
        pipeline: List[Dict] = [],
        max_height: str = "128px",
        empty_text: str = None,
        show_icons: bool = True,
        widget_id: str = None,
    ):
        if show_icons:
            self._pipeline = []
            for aug in pipeline:
                aug["icon"] = aug_icon_map.get(aug["category"], "")
                self._pipeline.append(aug)

        else:
            self._pipeline = pipeline
        self._max_height = max_height
        self._empty_text = empty_text
        self._show_icons = show_icons
        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {
            "max_height": self._max_height,
        }

    def get_json_state(self):
        return {"pipeline": self._pipeline}

    def set(self, pipeline: List[Dict]):
        if self._show_icons:
            self._pipeline = []
            for aug in pipeline:
                aug["icon"] = aug_icon_map.get(aug["category"], "")
                self._pipeline.append(aug)
        else:
            self._pipeline = pipeline
        StateJson()[self.widget_id] = self.get_json_state()
        StateJson().send_changes()

    def get(self):
        return self._pipeline

from typing import List, Union, Dict

from supervisely.app.widgets import Widget
from supervisely import TagMeta, TagMetaCollection
from supervisely.annotation.tag_meta import TagValueType
from supervisely.app.content import DataJson, StateJson
from supervisely.imaging.color import rgb2hex


VALUE_TYPE_NAME = {
    str(TagValueType.NONE): "NONE",
    str(TagValueType.ANY_STRING): "TEXT",
    str(TagValueType.ONEOF_STRING): "ONE OF",
    str(TagValueType.ANY_NUMBER): "NUMBER",
}


class TagMetasList(Widget):
    class Routes:
        CHECKBOX_CHANGED = "checkbox_cb"

    def __init__(
        self,
        tag_metas: Union[List[TagMeta], TagMetaCollection] = [],
        max_width: int = 300,
        multiple: bool = False,
        widget_id: int = None,
    ):
        self._tag_metas = tag_metas
        self._max_width = self._get_max_width(max_width)
        self._multiple = multiple

        super().__init__(widget_id=widget_id, file_path=__file__)

    def _get_max_width(self, value):
        if value < 150:
            value = 150
        return f"{value}px"

    def get_json_data(self):
        return {
            "maxWidth": self._max_width,
            "tags": [
                {
                    "name": f"<b>{tag_meta.name}</b>",
                    "valueType": VALUE_TYPE_NAME[tag_meta.value_type],
                    "color": rgb2hex(tag_meta.color),
                }
                for tag_meta in self._tag_metas
            ],
        }

    def get_json_state(self) -> Dict:
        return {
            "selected": [False for _ in self._tag_metas],
        }

    def get_selected_tag_metas(self):
        return [
            tm
            for selected, tm in zip(StateJson()[self.widget_id]["selected"], self._tag_metas)
            if selected
        ]

    def set(self, tag_metas: Union[List[TagMeta], TagMetaCollection]):
        selected_names = [tm.name for tm in self.get_selected_tag_metas()]
        self._tag_metas = tag_metas
        DataJson()[self.widget_id] = self.get_json_data()
        DataJson().send_changes()
        StateJson()[self.widget_id]["selected"] = [
            tm.name in selected_names for tm in self._tag_metas
        ]
        StateJson().send_changes()

    def select_all(self):
        StateJson()[self.widget_id]["selected"] = [True for _ in self._tag_metas]
        StateJson().send_changes()

    def deselect_all(self):
        StateJson()[self.widget_id]["selected"] = [False for _ in self._tag_metas]
        StateJson().send_changes()

    def select(self, names: List[str]):
        selected = [tm.name in names for tm in self._tag_metas]
        StateJson()[self.widget_id]["selected"] = selected
        StateJson().send_changes()

    def deselect(self, names: List[str]):
        selected = StateJson()[self.widget_id]["selected"]
        for idx, tm in enumerate(self._tag_metas):
            if tm.name in names:
                selected[idx] = False
        StateJson()[self.widget_id]["selected"] = selected
        StateJson().send_changes()

    def get_all_tag_metas(self):
        return self._tag_metas

    def selection_changed(self, func):
        route_path = self.get_route_path(TagMetasList.Routes.CHECKBOX_CHANGED)
        server = self._sly_app.get_server()
        self._checkboxes_handled = True

        @server.post(route_path)
        def _click():
            selected = self.get_selected_tag_metas()
            func(selected)

        return _click

from typing import List, Optional
from supervisely.app.widgets import Widget
from supervisely.app import DataJson


class LayersList(Widget):
    def __init__(
        self,
        layers: List[str],
        widget_id: Optional[str] = None,
    ):
        self._click_handled = False
        self._remove_click_handled = False
        self._layers = layers

        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {"layers": self._layers}

    def get_json_state(self):
        return {}

    def set(self, layers: List[str]):
        self._layers = layers
        self.update_data()
        DataJson().send_changes()

    def remove_click(self, func):
        # from fastapi import Request

        route_path = self.get_route_path("remove_button_clicked_cb")
        server = self._sly_app.get_server()
        self._remove_click_handled = True

        @server.post(route_path + "/{idx}")
        def _click(idx: int):
            func(idx)

        return _click
    
    def click(self, func):
        # from fastapi import Request

        route_path = self.get_route_path("button_clicked_cb")
        server = self._sly_app.get_server()
        self._click_handled = True

        @server.post(route_path + "/{idx}")
        def _click(idx: int):
            func(idx)

        return _click

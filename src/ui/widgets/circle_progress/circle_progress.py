from typing import Callable, Literal
from supervisely.app.widgets import Widget, Progress
from supervisely.app.content import DataJson


class CircleProgress(Widget):
    class Routes:
        CLICK = "clicked_cb"

    def __init__(self, progress: Progress, widget_id=None):
        self.progress = progress
        self._click_handled = False
        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {
            "status": None,
        }

    def get_json_state(self):
        return {}

    def set_status(self, status: Literal["success", "exception", "none"]):
        if status == "none":
            status = None
        DataJson()[self.widget_id]["status"] = status
        DataJson().send_changes()

    def click(self, func: Callable[[], None]) -> Callable[[], None]:
        """Decorator that allows to handle button click. Decorated function
        will be called on button click.

        :param func: Function to be called on button click.
        :type func: Callable
        :return: Decorated function.
        :rtype: Callable
        """
        route_path = self.get_route_path(CircleProgress.Routes.CLICK)
        server = self._sly_app.get_server()
        self._click_handled = True

        @server.post(route_path)
        def _click():
            try:
                func()
            except Exception as e:
                raise e

        return _click

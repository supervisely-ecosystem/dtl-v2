from supervisely.app.widgets import Widget


class ApplyCss(Widget):
    def __init__(self, css_url: str, content: Widget, widget_id: str = None):
        self._css_url = css_url
        self._content = content
        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {}

    def get_json_state(self):
        return {}

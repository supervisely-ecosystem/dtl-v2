from supervisely.app.widgets import Widget, Button


class LayerCard(Widget):
    def __init__(self, name: str, key: str, icon: str, color: str = None, widget_id: int = None):
        self._name = name
        self._key = key
        self._icon = icon
        self._color = color

        self._add_button = Button(
            "",
            icon="zmdi zmdi-plus-circle-o",
            button_type="text",
            style="color: black; margin-left: auto; padding: 10px",
        )

        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {
            "name": self._name,
            "icon": self._icon,
            "color": self._color,
        }

    def get_json_state(self):
        return {}

    def on_add_button(self, func):
        self._add_button.click(func)

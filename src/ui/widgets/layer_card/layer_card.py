from supervisely.app.widgets import Widget, Button, Icons, Dialog, Select


class LayerCard(Widget):
    def __init__(
        self,
        name: str,
        key: str,
        icon: str,
        dialog_widget: Dialog,
        selector_widget: Select,
        color: str = None,
        widget_id: int = None,
    ):
        self._name = name
        self._key = key
        self._icon = icon
        self._color = color
        self._dialog_widget = dialog_widget
        self._selector_widget = selector_widget

        self._open_docs = Button(
            "", icon="zmdi zmdi-help-outline", button_type="text"  # , style="color: gray;"
        )

        @self._open_docs.click
        def on_open_docs():
            self._selector_widget.set_value(self._key)
            self._dialog_widget.show()

        self._add_button = Button(
            "",
            icon="zmdi zmdi-plus",
            button_type="text",
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

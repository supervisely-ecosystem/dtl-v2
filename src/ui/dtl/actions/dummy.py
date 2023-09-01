from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely.app.widgets import NodesFlow


class DummyAction(Action):
    name = "dummy"
    title = "Dummy"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/dummy"
    description = "This layer (dummy) does nothing. Literally. Dummy layer can be useful when you have many destinations of other layers you want to merge into one."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {}

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {}

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
        ]
        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=None,
            get_dst=None,
            set_settings_from_json=None,
            id=layer_id,
        )

from typing import Optional

from supervisely.app.widgets import (
    NodesFlow,
    InputNumber,
    Select,
    Field,
)
from src.ui.dtl.Layer import Layer
from src.ui.dtl import ImgAugAugmentationsAction


class ImgAugCorruptLikeAction(ImgAugAugmentationsAction):
    name = "iaa_imgaug_corruptlike"
    options = {}

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        options_selector = Select(
            items=[Select.Item(value=v, label=l) for v, l in cls.options.items()],
            size="small",
        )
        options_field = Field(
            title="Augmentation option",
            description="",
            content=options_selector,
        )
        severity_input = InputNumber(value=2, min=1, max=5, step=1, size="small")
        severity_field = Field(
            title="Severity",
            description="",
            content=severity_input,
        )

        def get_settings(options_json: dict) -> dict:
            return {"option": options_selector.get_value(), "severity": severity_input.get_value()}

        def _set_settings_from_json(settings: dict):
            severity = settings.get("severity", 2)
            severity_input.value = severity

            default_option = None
            if len(cls.options) > 0:
                default_option = list(cls.options.keys())[0]
            option = settings.get("option", default_option)
            options_selector.set_value(option)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Augmentation option",
                    option_component=NodesFlow.WidgetOptionComponent(options_field),
                ),
                NodesFlow.Node.Option(
                    name="Severity",
                    option_component=NodesFlow.WidgetOptionComponent(severity_field),
                ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=True,
        )

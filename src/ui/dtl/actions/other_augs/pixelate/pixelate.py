from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAugmentationsAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs

from supervisely.app.widgets import (
    NodesFlow,
    InputNumber,
    Field,
)


class PixelateAction(OtherAugmentationsAction):
    name = "pixelate"
    title = "Pixelate"
    docs_url = (
        "https://imgaug.readthedocs.io/en/latest/source/overview/imgcorruptlike.html#pixelate"
    )
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        severity_input = InputNumber(value=2, min=1, max=5, step=1, size="small")
        severity_field = Field(
            title="Severity",
            description="",
            content=severity_input,
        )

        def get_settings(options_json: dict) -> dict:
            return {"severity": severity_input.get_value()}

        def _set_settings_from_json(settings: dict):
            severity = settings.get("severity", 2)
            severity_input.value = severity

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
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

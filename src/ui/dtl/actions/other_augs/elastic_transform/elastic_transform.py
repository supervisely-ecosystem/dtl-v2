from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAugmentationsAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size

from supervisely.app.widgets import (
    Text,
    NodesFlow,
    InputNumber,
    Field,
)


class ElasticTransformAction(OtherAugmentationsAction):
    name = "elastic_transform"
    title = "Elastic Transform"
    docs_url = ""
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        alpha_text = Text("Alpha", status="text", font_size=get_text_font_size())
        alpha_input = InputNumber(value=10.000, step=0.1, precision=3, controls=True, size="small")

        sigma_text = Text("Sigma", status="text", font_size=get_text_font_size())
        sigma_input = InputNumber(value=1.000, step=0.1, controls=True, size="small")

        def get_settings(options_json: dict) -> dict:
            return {"alpha": alpha_input.get_value(), "sigma": sigma_input.get_value()}

        def _set_settings_from_json(settings: dict):
            alpha_input.value = settings.get("alpha", 10)
            sigma_input.value = settings.get("sigma", 1)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="alpha_text",
                    option_component=NodesFlow.WidgetOptionComponent(alpha_text),
                ),
                NodesFlow.Node.Option(
                    name="alpha",
                    option_component=NodesFlow.WidgetOptionComponent(alpha_input),
                ),
                NodesFlow.Node.Option(
                    name="sigma_text",
                    option_component=NodesFlow.WidgetOptionComponent(sigma_text),
                ),
                NodesFlow.Node.Option(
                    name="sigma",
                    option_component=NodesFlow.WidgetOptionComponent(sigma_input),
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

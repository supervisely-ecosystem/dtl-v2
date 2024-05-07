from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs


class CopyAction(OtherAction):
    name = "copy"
    title = "Copy"
    docs_url = ""
    description = "Copies the input data to the selected destination."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        def get_settings(options_json: dict) -> dict:
            return {}

        def create_options(src: list, dst: list, settings: dict) -> dict:
            return {
                "src": [],
                "dst": [],
                "settings": [],
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=False,
        )

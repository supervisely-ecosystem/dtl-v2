from typing import Optional
import os
from pathlib import Path

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer


class DummyAction(OtherAction):
    name = "dummy"
    title = "Dummy"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/dummy"
    description = "This layer (dummy) does nothing. Literally. Dummy layer can be useful when you have many destinations of other layers you want to merge into one."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

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
        )

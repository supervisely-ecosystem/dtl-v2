from typing import Optional
import os
from pathlib import Path

from supervisely.app.widgets import NodesFlow

from src.ui.dtl import SpatialLevelAction
from src.ui.dtl.Layer import Layer


class RotateAction(SpatialLevelAction):
    name = "rotate"
    title = "Rotate"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/rotate"
    description = "Rotate layer (rotate) rotates images and its annotations."

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
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "rotate_angles": {
                    "min_degrees": options_json["min_degrees"],
                    "max_degrees": options_json["max_degrees"],
                },
                "black_regions": {"mode": options_json["black_regions"]},
            }

        def create_options(src: list, dst: list, settings: dict) -> dict:
            min_degrees_val = settings.get("rotate_angles", {}).get("min_degrees", 45)
            max_degrees_val = settings.get("rotate_angles", {}).get("max_degrees", 45)
            black_regions_val = settings.get("black_regions", {}).get("mode", "keep")
            settings_options = [
                NodesFlow.Node.Option(
                    name="rotate_angles_text",
                    option_component=NodesFlow.TextOptionComponent("Rotate Angles"),
                ),
                NodesFlow.Node.Option(
                    name="min_degrees_text",
                    option_component=NodesFlow.TextOptionComponent("Min Degrees"),
                ),
                NodesFlow.Node.Option(
                    name="min_degrees",
                    option_component=NodesFlow.IntegerOptionComponent(
                        default_value=min_degrees_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="max_degrees_text",
                    option_component=NodesFlow.TextOptionComponent("Max Degrees"),
                ),
                NodesFlow.Node.Option(
                    name="max_degrees",
                    option_component=NodesFlow.IntegerOptionComponent(
                        default_value=max_degrees_val
                    ),
                ),
                NodesFlow.Node.Option(
                    name="black_regions_text",
                    option_component=NodesFlow.TextOptionComponent("Black Regions"),
                ),
                NodesFlow.Node.Option(
                    name="black_regions",
                    option_component=NodesFlow.SelectOptionComponent(
                        items=[
                            NodesFlow.SelectOptionComponent.Item("keep", "Keep"),
                            NodesFlow.SelectOptionComponent.Item("crop", "Crop"),
                            NodesFlow.SelectOptionComponent.Item("preserve_size", "Preserve Size"),
                        ],
                        default_value=black_regions_val,
                    ),
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
        )

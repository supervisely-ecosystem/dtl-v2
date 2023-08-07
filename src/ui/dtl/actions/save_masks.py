import json
from .base import Action
from supervisely.app.widgets import NodesFlow


class SaveMasksAction(Action):
    name = "save_masks"
    title = "Save Masks"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/save-layers/save_masks"
    )
    description = "Save masks layer (save_masks) gives you an opportunity to get masked representations of data besides just images and annotations that you can get using save layer. It includes machine and human representations. In machine masks each of listed classes are colored in shades of gray that you specify. Note that black color [0, 0, 0] is automatically assigned with the background. In human masks you would get stacked original images with that images having class colors above."

    @classmethod
    def create_options(cls):
        return [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        cls.create_info_widget()
                    )
                ),
            ),
            NodesFlow.Node.Option(
                name="destination_text",
                option_component=NodesFlow.TextOptionComponent("Destination"),
            ),
            NodesFlow.Node.Option(
                name="dst", option_component=NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="Masks human",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="gt_human_color_text",
                option_component=NodesFlow.TextOptionComponent("Human masks labels colors"),
            ),
            NodesFlow.Node.Option(
                name="gt_human_color", option_component=NodesFlow.InputOptionComponent()
            ),
            NodesFlow.Node.Option(
                name="Masks machine",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="gt_machine_color_text",
                option_component=NodesFlow.TextOptionComponent("Machine masks labels colors"),
            ),
            NodesFlow.Node.Option(
                name="gt_machine_color", option_component=NodesFlow.InputOptionComponent()
            ),
        ]

    @classmethod
    def create_outputs(cls):
        return []
    
    @classmethod
    def parse_options(cls, options: dict) -> dict:
        dst = options["src"]
        if dst is None or dst == "":
            raise ValueError("Destination is not specified")
        if dst[0] == "[":
            dst = json.loads(dst)
        else:
            dst = [dst.strip("'\"")]
        return {
            "dst": dst,
            "settings": {},
        }

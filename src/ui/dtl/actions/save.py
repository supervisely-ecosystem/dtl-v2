from .base import Action
from supervisely.app.widgets import NodesFlow


class SaveAction(Action):
    name = "save"
    title = "Save"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/save"
    description = (
        "Save layer (save) allows to export annotations and images. Annotations are "
        "stored in .json files. Images are stored in .png or .jpg files (due to format"
        " of source image). When exporting annotations, meta.json file containing all "
        "used classes for project is also exported. Moreover, you can get visual "
        "representations of all annotated objects on top of your images by setting "
        "visualize to true."
    )

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
                name="Visualize",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
        ]

    @classmethod
    def create_outputs(cls):
        return []

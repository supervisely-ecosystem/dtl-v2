from .base import Action
from supervisely.app.widgets import NodesFlow


class SkeletonizeAction(Action):
    name = "skeletonize"
    title = "Skeletonize"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/skeletonize"
    description = "This layer (skeletonize) extracts skeletons from bitmap figures."

    @classmethod
    def create_options(cls):
        methods = [
            ("skeletonization", "Skeletonization"),
            ("medial_axis", "Medial axis"),
            ("thinning", "Thinning"),
        ]
        items = [NodesFlow.SelectOptionComponent.Item(*method) for method in methods]

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
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes to apply transformation"),
            ),
            NodesFlow.Node.Option(
                name="classes",
                option_component=NodesFlow.InputOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="method_text",
                option_component=NodesFlow.TextOptionComponent("Method"),
            ),
            NodesFlow.Node.Option(
                name="method",
                option_component=NodesFlow.SelectOptionComponent(items=items, default_value=items[0].value),
            ),
        ]

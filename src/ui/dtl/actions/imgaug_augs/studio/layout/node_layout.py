from typing import List
from supervisely.app.widgets import NodesFlow, Container, Field


def create_node_layout(
    pipeline_layout_container: Container,
    pipeline_sidebar_field: Field,
) -> List[NodesFlow.Node.Option]:
    settings_options = [
        NodesFlow.Node.Option(
            name="Augmentation Pipeline",
            option_component=NodesFlow.WidgetOptionComponent(
                widget=pipeline_layout_container,
                sidebar_component=NodesFlow.WidgetOptionComponent(pipeline_sidebar_field),
                sidebar_width=420,
            ),
        ),
    ]

    return settings_options

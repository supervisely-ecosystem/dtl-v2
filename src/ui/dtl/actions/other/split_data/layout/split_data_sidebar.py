from supervisely.app.widgets import (
    Container,
    Button,
    Field,
    Select,
    Input,
    Text,
    FileThumbnail,
    Card,
)


def create_sidebar_widgets():
    # Sidebar Initialization widgets
    sidebar_items = [
        Select.Item(0, "by percent"),
        Select.Item(1, "by number"),
        Select.Item(2, "by classes"),
        Select.Item(3, "by tags"),
    ]
    sidebar_selector = Select(sidebar_items)
    sidebar_selector_field = Field(
        sidebar_selector,
        "How to split data",
        "Select on which basis want your data to be distributed across datasets",
    )

    return (sidebar_selector, sidebar_selector_field)

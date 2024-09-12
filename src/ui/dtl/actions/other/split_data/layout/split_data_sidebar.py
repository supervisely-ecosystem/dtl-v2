from supervisely.app.widgets import (
    Container,
    Button,
    Field,
    Select,
    Input,
    Text,
    FileThumbnail,
    Card,
    Slider,
    InputNumber,
)
from src.ui.widgets import ClassesList, TagsList


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

    sidebar_percent_slider = Slider()
    sidebar_percent_field = Field(
        sidebar_percent_slider,
        "Select percentage",
        "Select percentage by which to distribute images across datasets",
    )
    sidebar_percent_field.hide()

    sidebar_number_input = InputNumber(min=1, max=100)
    sidebar_number_field = Field(
        sidebar_number_input,
        "Select number of images",
        "Select number of images to include in datasets",
    )
    sidebar_number_field.hide()

    sidebar_classes = ClassesList(multiple=True)
    sidebar_classes_field = Field(
        sidebar_classes, "Select classes", "Select classes with which to create datasets"
    )
    sidebar_classes_field.hide()

    sidebar_tags = TagsList(multiple=True)
    sidebar_tags_field = Field(
        sidebar_tags, "Select tags", "Select tags with which to create datasets"
    )
    sidebar_tags_field.hide()

    sidebar_container = Container(
        [
            sidebar_selector_field,
            sidebar_percent_field,
            sidebar_number_field,
            sidebar_classes_field,
            sidebar_tags_field,
        ]
    )  # TODO пофиксить лесенку

    return (
        sidebar_selector,
        sidebar_selector_field,
        sidebar_percent_field,
        sidebar_number_field,
        sidebar_classes,
        sidebar_classes_field,
        sidebar_tags,
        sidebar_tags_field,
        sidebar_container,
    )

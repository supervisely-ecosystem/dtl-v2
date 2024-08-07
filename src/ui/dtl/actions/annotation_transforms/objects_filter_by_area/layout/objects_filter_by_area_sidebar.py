from supervisely.app.widgets import Container
from supervisely.app.widgets import Select, Container, InputNumber, Field
from src.ui.dtl.utils import create_save_btn
from src.ui.widgets import ClassesList, InputTagList


def create_sidebar_widgets():
    # Sidebar Classes
    sidebar_classes = ClassesList(multiple=True)
    sidebar_classes_field = Field(
        title="Classes",
        content=sidebar_classes,
        description="Select the classes for which you want to set filtering criteria",
    )
    # --------------------------------

    # Sidebar Area
    sidebar_area_input = InputNumber(min=0, value=100)
    sidebar_area_input_field = Field(
        title="Input size",
        description="Filter annotations by area size in pixels.",
        content=sidebar_area_input,
    )
    # --------------------------------

    # Sidebar Comparator
    sidebar_comparator_select = Select(
        items=[Select.Item("lt", "Less"), Select.Item("gt", "Greater")],
        size="small",
    )
    sidebar_comparator_select_field = Field(
        title="Comparator",
        description="Select the comparator. If the selected area is less than or greater than the specified value, the annotation will be filtered.",
        content=sidebar_comparator_select,
    )
    # --------------------------------

    # Sidebar Action
    sidebar_action_select = Select(
        items=[
            Select.Item("delete", "Delete"),
            Select.Item("keep", "Keep"),
            Select.Item("add_tags", "Add tags"),
        ],
        size="small",
    )
    sidebar_action_select_field = Field(
        title="Action",
        description=(
            "Select the action to be applied to the filtered annotations. \n"
            "\nDelete - delete the filtered annotations. \n"
            "\nKeep - keep the filtered annotations, other annotations will be deleted. \n"
            "\nAdd tags - add tags to the filtered annotations, other annotations will not be deleted."
        ),
        content=sidebar_action_select,
    )
    # --------------------------------

    # Sidebar Tags
    sidebar_tags = InputTagList(multiple=True)
    sidebar_tags_field = Field(
        title="Tags",
        description="Select the tags to be added to the filtered annotations",
        content=sidebar_tags,
    )
    sidebar_tags_field.hide()
    # --------------------------------

    # Sidebar Save button
    sidebar_save_btn = create_save_btn()

    # Sidebar
    sidebar_container = Container(
        widgets=[
            sidebar_classes_field,
            sidebar_area_input_field,
            sidebar_comparator_select_field,
            sidebar_action_select_field,
            sidebar_tags_field,
            sidebar_save_btn,
        ]
    )

    return (
        # Sidebar Classes
        sidebar_classes,
        sidebar_classes_field,
        # Sidebar Area
        sidebar_area_input,
        sidebar_area_input_field,
        # Sidebar Comparator
        sidebar_comparator_select,
        sidebar_comparator_select_field,
        # Sidebar Action
        sidebar_action_select,
        sidebar_action_select_field,
        # Sidebar Tags
        sidebar_tags,
        sidebar_tags_field,
        # Sidebar Save button
        sidebar_save_btn,
        # Sidebar
        sidebar_container,
    )

from src.ui.dtl.utils import (
    create_save_btn,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
)
from supervisely.app.widgets import (
    Button,
    Container,
    Text,
    Field,
    InputNumber,
    Checkbox,
    Flexbox,
    Select,
    OneOf,
)


# objects_limit_per_image = (None,)
# tags_limit_per_image = (None,)
# include_images_with_tags = (None,)
# exclude_images_with_tags = (None,)


def create_job_filters_widgets() -> tuple:
    # SIDEBAR SETTINGS
    # OBJECTS LIMIT PER ITEM
    lj_filters_objects_limit_per_item_widget = InputNumber(
        value=0, step=1, size="small", controls=True
    )
    lj_filters_objects_limit_per_item_widget.hide()

    lj_filters_objects_limit_checkbox = Checkbox("Not applied", checked=True)
    lj_filters_objects_limit_container = Container(
        [lj_filters_objects_limit_checkbox, lj_filters_objects_limit_per_item_widget]
    )
    lj_filters_objects_limit_field = Field(
        title="Objects Limit Per Item",
        description="Select objects limit per item that will be available to annotators",
        content=lj_filters_objects_limit_container,
    )
    # ----------------------------

    # TAGS LIMIT PER ITEM
    lj_filters_tags_limit_per_item_widget = InputNumber(
        value=0, step=1, size="small", controls=True
    )
    lj_filters_tags_limit_per_item_widget.hide()
    lj_filters_tags_limit_checkbox = Checkbox("Not applied", checked=True)

    lj_filters_tags_limit_container = Container(
        [lj_filters_tags_limit_checkbox, lj_filters_tags_limit_per_item_widget]
    )
    lj_filters_tags_limit_field = Field(
        title="Tags Limit Per Item",
        description="Select tags limit per item that will be available to annotators",
        content=lj_filters_tags_limit_container,
    )
    # ----------------------------

    # ITEMS RANGE
    lj_filters_items_range_checkbox = Checkbox("Select all items", checked=True)

    lj_filters_items_range_start = InputNumber(
        value=1, step=1, min=1, max=1, size="small", controls=True  # max len(items_ids)
    )
    lj_filters_items_range_separator = Text(" _ ", status="text", font_size=16)
    lj_filters_items_range_end = InputNumber(
        value=0, step=1, min=1, max=1, size="small", controls=True  # value/max len(items_ids)
    )
    lj_filters_items_range_container = Flexbox(
        [
            lj_filters_items_range_start,
            lj_filters_items_range_separator,
            lj_filters_items_range_end,
        ],
        gap=3,
        center_content=False,
    )
    lj_filters_items_range_container.hide()

    lj_filters_items_range_field = Field(
        title="Items Range",
        description="Select items range that will be available to annotators",
        content=Container([lj_filters_items_range_checkbox, lj_filters_items_range_container]),
    )
    # ----------------------------

    # ITEMS IDS
    lj_filters_items_ids_selector_items = []
    lj_filters_items_ids_selector = Select(
        items=lj_filters_items_ids_selector_items,
        placeholder="Select items",
        filterable=True,
        multiple=True,
        size="small",
    )
    lj_filters_items_ids_selector_field = Field(
        title="Select Items",
        description="Select items that will be available to annotators",
        content=lj_filters_items_ids_selector,
    )
    # ----------------------------

    # CONDITION SELECTOR
    lj_filters_save_btn = create_save_btn()

    lj_filters_condition_container = Container(
        [lj_filters_objects_limit_field, lj_filters_tags_limit_field, lj_filters_items_range_field]
    )
    lj_filters_items_container = Container([lj_filters_items_ids_selector_field])

    lj_filters_condition_selector_items = [
        Select.Item(value="condition", label="Condition", content=lj_filters_condition_container),
        Select.Item(value="items", label="Items", content=lj_filters_items_container),
    ]
    lj_filters_condition_selector = Select(lj_filters_condition_selector_items, size="small")
    lj_filters_condition_oneof = OneOf(lj_filters_condition_selector)

    lj_filters_condition_selector_field = Field(
        title="Select by",
        description="Select by condition",
        content=Container(
            [lj_filters_condition_selector, lj_filters_condition_oneof, lj_filters_save_btn]
        ),
    )
    # ----------------------------
    # ----------------------------

    # PREVIEW
    # TODO: add preview
    lj_filters_preview_text = Text("Select by:", "text", font_size=get_text_font_size())
    # ----------------------------

    # LAYOUT
    lj_filters_edit_text = Text("Filters", status="text", font_size=get_text_font_size())
    lj_filters_edit_btn = Button(
        text="EDIT",
        icon="zmdi zmdi-edit",
        button_type="text",
        button_size="small",
        emit_on_click="openSidebar",
        style=get_set_settings_button_style(),
    )
    lj_filters_edit_container = get_set_settings_container(
        lj_filters_edit_text, lj_filters_edit_btn
    )
    # ----------------------------

    return (
        # sidebar
        lj_filters_objects_limit_per_item_widget,
        lj_filters_objects_limit_checkbox,
        lj_filters_objects_limit_container,
        lj_filters_objects_limit_field,
        lj_filters_tags_limit_per_item_widget,
        lj_filters_tags_limit_checkbox,
        lj_filters_tags_limit_container,
        lj_filters_tags_limit_field,
        lj_filters_items_range_checkbox,
        lj_filters_items_range_start,
        lj_filters_items_range_separator,
        lj_filters_items_range_end,
        lj_filters_items_range_container,
        lj_filters_items_range_field,
        lj_filters_items_ids_selector_items,
        lj_filters_items_ids_selector,
        lj_filters_items_ids_selector_field,
        lj_filters_save_btn,
        lj_filters_condition_container,
        lj_filters_items_container,
        lj_filters_condition_selector_items,
        lj_filters_condition_selector,
        lj_filters_condition_oneof,
        lj_filters_condition_selector_field,
        # preview
        lj_filters_preview_text,
        # layout
        lj_filters_edit_text,
        lj_filters_edit_btn,
        lj_filters_edit_container,
    )

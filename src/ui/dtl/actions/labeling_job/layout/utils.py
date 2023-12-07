from supervisely.app.widgets import (
    Input,
    Text,
    Checkbox,
    Select,
    TextArea,
    InputNumber,
    SelectDataset,
)
from src.ui.widgets import ClassesList, ClassesListPreview, TagsList, TagsListPreview
from src.ui.dtl.utils import (
    get_layer_docs,
    get_text_font_size,
    classes_list_settings_changed_meta,
    set_classes_list_settings_from_json,
    set_classes_list_preview,
    get_classes_list_value,
    tags_list_settings_changed_meta,
    set_tags_list_settings_from_json,
    set_tags_list_preview,
    get_tags_list_value,
)


# SET PREVIEWS
# def set_lj_dataset_preview(lj_dataset_selector: SelectDataset, lj_dataset_name_preview: Text):
#     import src.globals as g

#     # TODO: add normal preview names
#     dataset_ids = lj_dataset_selector.get_selected_ids()
#     project_name = g.api.project.get_info_by_id(lj_dataset_selector.get_selected_project_id()).name
#     dataset_names = [g.api.dataset.get_info_by_id(dataset_id).name for dataset_id in dataset_ids]
#     dataset_preview_text = ""
#     if len(dataset_names) == 0:
#         lj_dataset_name_preview.set(f"Dataset: {project_name}/{dataset_names}", "text")
#     else:
#         dataset_preview_text = "".join(
#             f"<li>{project_name}/{ds_name}</li>" for ds_name in dataset_names
#         )
#         dataset_preview_text = (
#             f'<ul style="margin: 1px; padding: 0px 0px 0px 18px">{dataset_preview_text}<ul>'
#         )
#     lj_dataset_name_preview.set(dataset_preview_text, "text")


def set_lj_name_preview(lj_description_title_input: Input, lj_description_title_preview: Text):
    name = lj_description_title_input.get_value()
    if name is None:
        name = ""
    lj_description_title_preview.set(f"Title: {name}", "text")


def set_lj_reviewer_preview(
    lj_members_reviewer_selector: Select, lj_members_reviewer_preview: Text
):
    reviewer_login = lj_members_reviewer_selector.get_label()
    if reviewer_login is None:
        reviewer_login = "select reviewer in settings"
    lj_members_reviewer_preview.set(f"Reviewer: {reviewer_login}", "text")


def set_lj_labelers_preview(
    lj_members_labelers_selector: Select, lj_members_labelers_preview: Text
):
    user_logins = lj_members_labelers_selector.get_labels()
    if len(user_logins) == 0:
        user_logins = ["select annotators in settings"]
    lj_members_labelers_preview.set(f"Assigned to: {', '.join(user_logins)}", "text")


def set_lj_filter_preview(
    # lj_filters_condition_selector: Select,
    # lj_filters_condition_preview_text: Text,
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_objects_limit_preview_text: Text,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_preview_text: Text,
    # lj_filters_items_range_checkbox: Checkbox,
    # lj_filters_items_range_start: InputNumber,
    # lj_filters_items_range_end: InputNumber,
    # lj_filters_items_range_preview_text: Text,
):
    # filter_condition = lj_filters_condition_selector.get_value()
    # if filter_condition == "items":
    #     lj_filters_condition_preview_text.set(f"Filter by: {filter_condition}", "text")
    #     lj_filters_objects_limit_preview_text.hide()
    #     lj_filters_tags_limit_preview_text.hide()
    #     lj_filters_items_range_preview_text.hide()
    # else:
    #     lj_filters_condition_preview_text.set(f"Filter by: {filter_condition}", "text")

    # tab right if uncomment above
    if lj_filters_objects_limit_checkbox.is_checked():
        lj_filters_objects_limit_preview_text.set("Objects limit per item: unlimited", "text")
    else:
        lj_filters_objects_limit_preview_text.set(
            f"Objects limit per item: {lj_filters_objects_limit_per_item_widget.value}", "text"
        )

    if lj_filters_tags_limit_checkbox.is_checked():
        lj_filters_tags_limit_preview_text.set("Tags limit per item: unlimited", "text")
    else:
        lj_filters_tags_limit_preview_text.set(
            f"Tags limit per item: {lj_filters_tags_limit_per_item_widget.value}", "text"
        )

    # if lj_filters_items_range_checkbox.is_checked():
    #     lj_filters_items_range_preview_text.set("Items range: all items", "text")
    # else:
    #     lj_filters_items_range_preview_text.set(
    #         f"Items range: {lj_filters_items_range_start.value} - {lj_filters_items_range_end.value}",
    #         "text",
    #     )
    lj_filters_objects_limit_preview_text.show()
    lj_filters_tags_limit_preview_text.show()
    # lj_filters_items_range_preview_text.show()


# ----------------------------


# SETTINGS
def save_settings(
    # lj_dataset_selector: SelectDataset,
    lj_description_title_input: Input,
    lj_description_readme_editor: TextArea,
    lj_description_description_editor: TextArea,
    lj_members_reviewer_selector: Select,
    lj_members_labelers_selector: Select,
    lj_settings_classes_list_widget: ClassesList,
    lj_settings_tags_list_widget: TagsList,
    lj_filters_condition_selector: Select,
    lj_filters_items_ids_selector: Select,
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_filters_items_range_checkbox: Checkbox,
    lj_filters_items_range_start: InputNumber,
    lj_filters_items_range_end: InputNumber,
) -> dict:
    # init vars
    disable_objects_limit_per_item = None
    disable_tags_limit_per_item = None
    objects_limit_per_item = None
    tags_limit_per_item = None
    include_items_with_tags = None
    exclude_items_with_tags = None
    items_range = None
    items_ids = None

    # dataset_ids = lj_dataset_selector.get_selected_ids()
    dataset_ids = None

    name = lj_description_title_input.get_value()
    readme = lj_description_readme_editor.get_value()
    description = lj_description_description_editor.get_value()

    user_ids = lj_members_labelers_selector.get_value()
    reviewer_id = lj_members_reviewer_selector.get_value()

    classes_to_label = lj_settings_classes_list_widget.get_selected_classes()
    tags_to_label = lj_settings_tags_list_widget.get_selected_tags()

    filter_condition = lj_filters_condition_selector.get_value()
    if filter_condition == "items":
        items_ids = lj_filters_items_ids_selector.get_value()
    else:
        disable_objects_limit_per_item = lj_filters_objects_limit_checkbox.is_checked()
        if not disable_objects_limit_per_item:
            objects_limit_per_item = lj_filters_objects_limit_per_item_widget.value

        disable_tags_limit_per_item = lj_filters_tags_limit_checkbox.is_checked()
        if not disable_tags_limit_per_item:
            tags_limit_per_item = lj_filters_tags_limit_per_item_widget.value

        disable_items_range = lj_filters_items_range_checkbox.is_checked()
        if not disable_items_range:
            items_range = [
                lj_filters_items_range_start.value,
                lj_filters_items_range_end.value,
            ]

    return {
        # data
        "dataset_id": dataset_ids,
        # description
        "name": name,
        "description": description,
        "readme": readme,
        # members
        "user_ids": user_ids,
        "reviewer_id": reviewer_id,
        # classes
        "classes_to_label": classes_to_label,
        # tags
        "tags_to_label": tags_to_label,
        # filters
        "filter_condition": filter_condition,
        "disable_objects_limit_per_item": disable_objects_limit_per_item,
        "objects_limit_per_item": objects_limit_per_item,
        "disable_tags_limit_per_item": disable_tags_limit_per_item,
        "tags_limit_per_item": tags_limit_per_item,
        "include_items_with_tags": include_items_with_tags,
        "exclude_items_with_tags": exclude_items_with_tags,
        "disable_items_range": disable_items_range,
        "items_range": items_range,
        "items_ids": items_ids,
    }


# ----------------------------


# SET SETTINGS FROM JSON
def set_lj_name_from_json(settings: dict, lj_description_title_input: Input):
    name = settings.get("name", "Annotation Job")
    lj_description_title_input.set_value(name)


def set_lj_readme_from_json(settings: dict, lj_description_readme_editor: TextArea):
    readme = settings.get("readme", None)
    lj_description_readme_editor.set_value(readme)


def set_lj_description_from_json(settings: dict, lj_description_description_editor: TextArea):
    description = settings.get("description", None)
    lj_description_description_editor.set_value(description)


# TODO: set dataset_id from json
# def set_lj_dataset_id_from_json(settings: dict, dataset_selector: SelectDataset):
#     dataset_id = settings.get("dataset_id", None)
#     dataset_selector.set_dataset(dataset_id)


def set_lj_reviewer_from_json(settings: dict, lj_members_reviewer_selector: Select):
    reviewer_id = settings.get("reviewer_id", None)
    lj_members_reviewer_selector.set_value(reviewer_id)


def set_lj_labelers_from_json(settings: dict, lj_members_labelers_selector: Select):
    user_ids = settings.get("user_ids", [])
    lj_members_labelers_selector.set_value(user_ids)


def set_lj_filter_condition_from_json(settings: dict, lj_filters_condition_selector: Select):
    filter_condition = settings.get("filter_condition", "condition")
    lj_filters_condition_selector.set_value(filter_condition)


def set_lj_items_ids_from_json(settings: dict, lj_filters_items_ids_selector: Select):
    items_ids = settings.get("items_ids", None)
    lj_filters_items_ids_selector.set(items_ids)


def set_lj_objects_limit_per_item_from_json(
    settings: dict,
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
):
    disable_objects_limit_per_item = settings.get("disable_objects_limit_per_item", True)
    if disable_objects_limit_per_item:
        lj_filters_objects_limit_checkbox.check()
    else:
        lj_filters_objects_limit_checkbox.uncheck()
        objects_limit_per_item = settings.get("objects_limit_per_item", None)
        lj_filters_objects_limit_per_item_widget.value = objects_limit_per_item


def set_lj_tags_limit_per_item_from_json(
    settings: dict,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
):
    disable_tags_limit_per_item = settings.get("disable_tags_limit_per_item", True)
    if disable_tags_limit_per_item:
        disable_tags_limit_per_item = lj_filters_tags_limit_checkbox.check()
    else:
        lj_filters_tags_limit_checkbox.uncheck()
        tags_limit_per_item = settings.get("tags_limit_per_item", None)
        lj_filters_tags_limit_per_item_widget.value = tags_limit_per_item


def set_lj_items_range_from_json(
    settings: dict,
    lj_filters_items_range_checkbox: Checkbox,
    lj_filters_items_range_start: InputNumber,
    lj_filters_items_range_end: InputNumber,
):
    disable_items_range = settings.get("disable_items_range", True)
    if disable_items_range:
        disable_items_range = lj_filters_items_range_checkbox.check()
    else:
        lj_filters_items_range_checkbox.uncheck()
        items_range = settings.get("items_range", None)
        lj_filters_items_range_start.value = items_range[0]
        lj_filters_items_range_end.value = items_range[1]


def set_settings_from_json(
    settings: dict,
    lj_description_title_input: Input,
    lj_description_title_preview: Text,
    lj_description_readme_editor: TextArea,
    lj_description_description_editor: TextArea,
    lj_members_reviewer_selector: Select,
    lj_members_reviewer_preview: Text,
    lj_members_labelers_selector: Select,
    lj_members_labelers_preview: Text,
    lj_settings_classes_list_widget: ClassesList,
    lj_settings_classes_list_preview: ClassesListPreview,
    lj_settings_tags_list_widget: TagsList,
    lj_settings_tags_list_preview: TagsListPreview,
    lj_filters_condition_selector: Select,
    lj_filters_condition_preview_text: Text,
    lj_filters_items_ids_selector: Select,
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_items_range_preview_text: Text,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_preview_text: Text,
    lj_filters_items_range_checkbox: Checkbox,
    lj_filters_items_range_start: InputNumber,
    lj_filters_items_range_end: InputNumber,
    lj_filters_objects_limit_preview_text: Text,
) -> dict:
    # SET DATA
    # set_lj_dataset_id_from_json(settings)

    # SET DESCRPTION
    set_lj_name_from_json(settings, lj_description_title_input)
    set_lj_readme_from_json(settings, lj_description_readme_editor)
    set_lj_description_from_json(settings, lj_description_description_editor)

    set_lj_name_preview(lj_description_title_input, lj_description_title_preview)
    # ----------------------------

    # SET MEMBERS
    set_lj_reviewer_from_json(settings, lj_members_reviewer_selector)
    set_lj_labelers_from_json(settings, lj_members_labelers_selector)

    set_lj_reviewer_preview(lj_members_reviewer_selector, lj_members_reviewer_preview)
    set_lj_labelers_preview(lj_members_labelers_selector, lj_members_labelers_preview)
    # ----------------------------

    # SET CLASSES
    classes_settings = settings.get("classes_to_label", [])
    set_classes_list_settings_from_json(lj_settings_classes_list_widget, classes_settings)
    set_classes_list_preview(
        lj_settings_classes_list_widget, lj_settings_classes_list_preview, classes_settings
    )
    # ----------------------------

    # SET TAGS
    tags_settings = settings.get("tags_to_label", [])
    set_tags_list_settings_from_json(lj_settings_tags_list_widget, tags_settings)
    set_tags_list_preview(
        lj_settings_tags_list_widget, lj_settings_tags_list_preview, tags_settings
    )
    # ----------------------------

    # SET FILTERS
    set_lj_filter_condition_from_json(settings, lj_filters_condition_selector)
    set_lj_filter_preview(
        lj_filters_condition_selector,
        lj_filters_condition_preview_text,
        lj_filters_objects_limit_checkbox,
        lj_filters_objects_limit_per_item_widget,
        lj_filters_objects_limit_preview_text,
        lj_filters_tags_limit_checkbox,
        lj_filters_tags_limit_per_item_widget,
        lj_filters_tags_limit_preview_text,
        lj_filters_items_range_checkbox,
        lj_filters_items_range_start,
        lj_filters_items_range_end,
        lj_filters_items_range_preview_text,
    )

    filter_condition = lj_filters_condition_selector.get_value()
    if filter_condition == "items":
        set_lj_items_ids_from_json(settings, lj_filters_items_ids_selector)
    else:
        set_lj_objects_limit_per_item_from_json(
            settings, lj_filters_objects_limit_checkbox, lj_filters_objects_limit_per_item_widget
        )
        set_lj_tags_limit_per_item_from_json(
            settings, lj_filters_tags_limit_checkbox, lj_filters_tags_limit_per_item_widget
        )
        set_lj_items_range_from_json(
            settings,
            lj_filters_items_range_checkbox,
            lj_filters_items_range_start,
            lj_filters_items_range_end,
        )

        # TODO: add include/exclude items with tags
        # include_items_with_tags = None
        # exclude_items_with_tags = None


# ----------------------------

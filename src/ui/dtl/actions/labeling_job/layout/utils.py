from typing import List
from supervisely.app.widgets import (
    Button,
    Input,
    Text,
    Checkbox,
    Select,
    TextArea,
    InputNumber,
    NotificationBox,
)
from src.ui.widgets import ClassesList, ClassesListPreview, TagsList, TagsListPreview
from src.ui.dtl.utils import (
    set_classes_list_settings_from_json,
    set_classes_list_preview,
    set_tags_list_settings_from_json,
    set_tags_list_preview,
)


# SET PREVIEWS
def set_lj_name_preview(lj_description_title_input: Input, lj_description_title_preview: Text):
    name = lj_description_title_input.get_value()
    if name is None:
        name = ""
    lj_description_title_preview.set(
        f"<span style='padding-left: 14px'>Title: {name}</span>", "text"
    )


def set_lj_reviewer_preview(
    lj_members_reviewer_selector: Select, lj_members_reviewer_preview: Text
):
    reviewer_login = lj_members_reviewer_selector.get_label()
    if reviewer_login is None:
        formatted_login = "select reviewer in settings"
    else:
        formatted_login = f'<i class="zmdi zmdi-account"></i>&nbsp;{reviewer_login}'
    lj_members_reviewer_preview.set(
        f"<span style='padding-left: 14px'>Reviewer: {formatted_login}</span>", "text"
    )


def set_lj_labelers_preview(
    lj_members_labelers_selector: Select, lj_members_labelers_preview: Text
):
    user_logins = lj_members_labelers_selector.get_labels()
    if len(user_logins) == 0:
        formatted_logins = "select annotators in settings"
    elif len(user_logins) > 1:
        formatted_logins = f'<i class="zmdi zmdi-account"></i>&nbsp;{user_logins[0]}' + " ".join(
            f'<div style="padding-left: 89px;"><i class="zmdi zmdi-account"></i>&nbsp;{login}</div>'
            for login in user_logins[1:]
        )
    else:
        formatted_logins = f'<i class="zmdi zmdi-account"></i>&nbsp;{user_logins[0]}'
    lj_members_labelers_preview.set(
        f"<span style='padding-left: 14px'>Assigned to: {formatted_logins}</span>", "text"
    )


def set_lj_filter_preview(
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_objects_limit_preview_text: Text,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_preview_text: Text,
):
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

    lj_filters_objects_limit_preview_text.show()
    lj_filters_tags_limit_preview_text.show()


def set_lj_output_project_name_preview(
    lj_output_project_name_input: Input, lj_output_project_name_preview: Text
):
    project_name = lj_output_project_name_input.get_value()
    lj_output_project_name_preview.set(
        f"<span style='padding-left: 14px'>Project name: {project_name}</span>", "text"
    )


def set_lj_output_dataset_name_preview(
    lj_output_dataset_name_input: Input,
    lj_output_dataset_keep_checkbox: Checkbox,
    lj_output_dataset_name_preview: Text,
):
    keep_dataset = lj_output_dataset_keep_checkbox.is_checked()
    if keep_dataset:
        lj_output_dataset_name_preview.set(
            "<span style='padding-left: 14px'>Keep source datasets structure</span>",
            "text",
        )
    else:
        dataset_name = lj_output_dataset_name_input.get_value()
        lj_output_dataset_name_preview.set(
            f"<span style='padding-left: 14px'>Dataset name: {dataset_name}</span>", "text"
        )


def set_output_preview(
    modifies_data: bool,
    lj_output_edit_btn: Button,
    lj_output_modifies_data_preview: NotificationBox,
    lj_output_project_name_preview: Text,
    lj_output_dataset_name_preview: Text,
):
    if modifies_data:
        # show output options
        lj_output_modifies_data_preview.hide()
        lj_output_edit_btn.enable()
        lj_output_project_name_preview.show()
        lj_output_dataset_name_preview.show()
    else:
        # hide output options, show notification
        lj_output_edit_btn.disable()
        lj_output_project_name_preview.hide()
        lj_output_dataset_name_preview.hide()
        lj_output_modifies_data_preview.show()


# ----------------------------


# SETTINGS
def save_settings(
    # lj_dataset_selector: SelectDataset
    lj_description_title_input: Input,
    lj_description_readme_editor: TextArea,
    lj_description_description_editor: TextArea,
    lj_members_reviewer_selector: Select,
    lj_members_labelers_selector: Select,
    saved_classes_settings: List[str],
    saved_tags_settings: List[str],
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_output_project_name_input: Input,
    lj_output_dataset_keep_checkbox: Checkbox,
    lj_output_dataset_name_input: Input,
    modifies_data: bool,
) -> dict:
    # init vars
    disable_objects_limit_per_item = None
    disable_tags_limit_per_item = None
    objects_limit_per_item = None
    tags_limit_per_item = None
    include_items_with_tags = None
    exclude_items_with_tags = None

    name = lj_description_title_input.get_value()
    description = lj_description_description_editor.get_value()
    readme = lj_description_readme_editor.get_value()

    user_ids = lj_members_labelers_selector.get_value()
    if not isinstance(user_ids, list):
        user_ids = [user_ids]

    reviewer_id = lj_members_reviewer_selector.get_value()

    disable_objects_limit_per_item = lj_filters_objects_limit_checkbox.is_checked()
    if not disable_objects_limit_per_item:
        objects_limit_per_item = lj_filters_objects_limit_per_item_widget.value

    disable_tags_limit_per_item = lj_filters_tags_limit_checkbox.is_checked()
    if not disable_tags_limit_per_item:
        tags_limit_per_item = lj_filters_tags_limit_per_item_widget.value

    project_name = lj_output_project_name_input.get_value()

    if not modifies_data:
        dataset_name = None
        keep_original_ds = True
    else:
        keep_original_ds = lj_output_dataset_keep_checkbox.is_checked()
        if keep_original_ds:
            dataset_name = None
        else:
            dataset_name = lj_output_dataset_name_input.get_value()

    return {
        # description
        "job_name": name,
        "description": description,
        "readme": readme,
        # members
        "user_ids": user_ids,
        "reviewer_id": reviewer_id,
        # classes
        "classes_to_label": saved_classes_settings,
        # tags
        "tags_to_label": saved_tags_settings,
        # filters
        "disable_objects_limit_per_item": disable_objects_limit_per_item,
        "objects_limit_per_item": objects_limit_per_item,
        "disable_tags_limit_per_item": disable_tags_limit_per_item,
        "tags_limit_per_item": tags_limit_per_item,
        "include_items_with_tags": include_items_with_tags,
        "exclude_items_with_tags": exclude_items_with_tags,
        # output
        "create_new_project": modifies_data,
        "project_name": project_name,
        "dataset_name": dataset_name,
        "keep_original_ds": keep_original_ds,
    }


# ----------------------------


# SET SETTINGS FROM JSON
def set_lj_name_from_json(settings: dict, lj_description_title_input: Input):
    name = settings.get("job_name", "Annotation Job")
    lj_description_title_input.set_value(name)


def set_lj_readme_from_json(settings: dict, lj_description_readme_editor: TextArea):
    readme = settings.get("readme", None)
    lj_description_readme_editor.set_value(readme)


def set_lj_description_from_json(settings: dict, lj_description_description_editor: TextArea):
    description = settings.get("description", None)
    lj_description_description_editor.set_value(description)


def set_lj_reviewer_from_json(settings: dict, lj_members_reviewer_selector: Select):
    reviewer_id = settings.get("reviewer_id", None)
    lj_members_reviewer_selector.set_value(reviewer_id)


def set_lj_labelers_from_json(settings: dict, lj_members_labelers_selector: Select):
    user_ids = settings.get("user_ids", [])
    lj_members_labelers_selector.set_value(user_ids)


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


def set_output_project_name_from_json(settings: dict, lj_output_project_name_input: Input):
    project_name = settings.get("project_name", "")
    lj_output_project_name_input.set_value(project_name)


def set_output_dataset_name_from_json(
    settings: dict,
    lj_output_dataset_name_input: Input,
    lj_output_dataset_keep_checkbox: Checkbox,
):
    keep_original_ds = settings.get("keep_original_ds", False)
    if keep_original_ds:
        lj_output_dataset_name_input.hide()
        lj_output_dataset_keep_checkbox.check()
    else:
        lj_output_dataset_name_input.show()
        lj_output_dataset_keep_checkbox.uncheck()
    dataset_name = settings.get("dataset_name", "")
    lj_output_dataset_name_input.set_value(dataset_name)


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
    lj_filters_objects_limit_checkbox: Checkbox,
    lj_filters_objects_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_checkbox: Checkbox,
    lj_filters_tags_limit_per_item_widget: InputNumber,
    lj_filters_tags_limit_preview_text: Text,
    lj_filters_objects_limit_preview_text: Text,
    lj_output_project_name_input: Input,
    lj_output_dataset_keep_checkbox: Checkbox,
    lj_output_dataset_name_input: Input,
    lj_output_project_name_preview: Text,
    lj_output_dataset_name_preview: Text,
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
    set_lj_filter_preview(
        lj_filters_objects_limit_checkbox,
        lj_filters_objects_limit_per_item_widget,
        lj_filters_objects_limit_preview_text,
        lj_filters_tags_limit_checkbox,
        lj_filters_tags_limit_per_item_widget,
        lj_filters_tags_limit_preview_text,
    )

    set_lj_objects_limit_per_item_from_json(
        settings, lj_filters_objects_limit_checkbox, lj_filters_objects_limit_per_item_widget
    )
    set_lj_tags_limit_per_item_from_json(
        settings, lj_filters_tags_limit_checkbox, lj_filters_tags_limit_per_item_widget
    )
    # ----------------------------

    # SET OUTPUT
    set_output_project_name_from_json(settings, lj_output_project_name_input)
    set_output_dataset_name_from_json(
        settings, lj_output_dataset_name_input, lj_output_dataset_keep_checkbox
    )

    set_lj_output_project_name_preview(lj_output_project_name_input, lj_output_project_name_preview)
    set_lj_output_dataset_name_preview(
        lj_output_dataset_name_input,
        lj_output_dataset_keep_checkbox,
        lj_output_dataset_name_preview,
    )
    # ----------------------------

    # TODO: add include/exclude items with tags
    # include_items_with_tags = None
    # exclude_items_with_tags = None


# ----------------------------

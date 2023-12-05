from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta
from supervisely.app.widgets import NodesFlow, Text, Input, Checkbox

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size

import src.globals as g

# g.api.labeling_job.create(
#     name
#     dataset_id
#     user_ids
#     readme
#     description
#     classes_to_label
#     objects_limit_per_image
#     tags_to_label
#     tags_limit_per_image
#     include_images_with_tags
#     exclude_images_with_tags
#     images_range
#     reviewer_id
#     images_ids
# )

# name: str,
# dataset_id: int,
# user_ids: List[int],
# readme: Optional[str] = None,
# description: Optional[str] = None,
# classes_to_label: Optional[List[str]] = None,
# objects_limit_per_image: Optional[int] = None,
# tags_to_label: Optional[List[str]] = None,
# tags_limit_per_image: Optional[int] = None,
# include_images_with_tags: Optional[List[str]] = None,
# exclude_images_with_tags: Optional[List[str]] = None,
# images_range: Optional[List[int, int]] = None,
# reviewer_id: Optional[int] = None,
# images_ids: Optional[List[int]] = [],


from src.ui.dtl.actions.labeling_job.layout.job_description import create_job_description_widgets
from src.ui.dtl.actions.labeling_job.layout.job_members import create_job_members_widgets
from src.ui.dtl.actions.labeling_job.layout.job_settings_classes import (
    create_job_settings_classes_widgets,
)
from src.ui.dtl.actions.labeling_job.layout.job_settings_tags import (
    create_job_settings_tags_widgets,
)
from src.ui.dtl.actions.labeling_job.layout.job_filters import create_job_filters_widgets
from src.ui.dtl.actions.labeling_job.layout.layout import create_settings_options


class LabelingJobAction(OtherAction):
    name = "labeling_job"
    title = "Create Labeling Job"
    docs_url = ""
    description = "Creates Labeling Job with given parameters."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()

        saved_classes_settings = "default"
        saved_tags_settings = "default"

        # DESCRIPTION
        (
            # sidebar
            lj_description_title_field,
            lj_description_title_input,
            lj_description_description_field,
            lj_description_description_editor,
            lj_description_readme_field,
            lj_description_readme_editor,
            lj_description_markdown_support_text,
            lj_description_save_btn,
            lj_description_sidebar_container,
            # preview
            lj_description_title_preview,
            # layout
            lj_description_text,
            lj_description_edit_btn,
            lj_description_container,
        ) = create_job_description_widgets()

        # DESCRIPTION CBs
        @lj_description_save_btn.click
        def description_save_btn_cb():
            return

        # ----------------------------

        # MEMBERS
        (
            # sidebar
            lj_members_items,
            lj_members_reviewer_field,
            lj_members_reviewer_selector,
            lj_members_labelers_field,
            lj_members_labelers_selector,
            lj_members_save_btn,
            lj_members_sidebar_container,
            # preview
            lj_members_reviewer_preview,
            lj_members_labelers_preview,
            lj_members_preview_container,
            # layout
            lj_members_text,
            lj_members_edit_btn,
            lj_members_container,
        ) = create_job_members_widgets()

        # MEMBERS CBs
        @lj_members_save_btn.click
        def members_save_btn_cb():
            return

        # ----------------------------

        # CLASSES
        (
            # sidebar
            lj_settings_classes_list_widget_notification,
            lj_settings_classes_list_widget,
            lj_settings_classes_list_save_btn,
            lj_settings_classes_list_set_default_btn,
            lj_settings_classes_list_widget_field,
            lj_settings_classes_list_widgets_container,
            # preview
            lj_settings_classes_list_preview,
            # layout
            lj_settings_classes_list_edit_text,
            lj_settings_classes_list_edit_btn,
            lj_settings_classes_list_edit_container,
        ) = create_job_settings_classes_widgets()

        # CLASSES CBs
        @lj_settings_classes_list_save_btn.click
        def classes_save_btn_cb():
            return

        @lj_settings_classes_list_set_default_btn.click
        def classes_set_default_btn_cb():
            return

        # ----------------------------

        # TAGS
        (
            # sidebar
            lj_settings_tags_list_widget_notification,
            lj_settings_tags_list_widget,
            lj_settings_tags_list_save_btn,
            lj_settings_tags_list_set_default_btn,
            lj_settings_tags_list_widget_field,
            lj_settings_tags_list_widgets_container,
            # preview
            lj_settings_tags_list_preview,
            # layout
            lj_settings_tags_list_edit_text,
            lj_settings_tags_list_edit_btn,
            lj_settings_tags_list_edit_container,
        ) = create_job_settings_tags_widgets()

        # TAGS CBs
        @lj_settings_tags_list_save_btn.click
        def tags_save_btn_cb():
            return

        @lj_settings_tags_list_set_default_btn.click
        def tags_set_default_btn_cb():
            return

        # ----------------------------

        # FILTERS
        (
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
        ) = create_job_filters_widgets()

        # FILTERS CBs
        @lj_filters_objects_limit_checkbox.value_changed
        def objects_limit_checkbox_cb(is_checked):
            if is_checked:
                lj_filters_objects_limit_per_item_widget.hide()
            else:
                lj_filters_objects_limit_per_item_widget.show()

        @lj_filters_tags_limit_checkbox.value_changed
        def tags_limit_checkbox_cb(is_checked):
            if is_checked:
                lj_filters_tags_limit_per_item_widget.hide()
            else:
                lj_filters_tags_limit_per_item_widget.show()

        @lj_filters_items_range_checkbox.value_changed
        def items_range_checkbox_cb(is_checked):
            if is_checked:
                lj_filters_items_range_container.hide()
            else:
                lj_filters_items_range_container.show()

        @lj_filters_save_btn.click
        def filters_save_btn_cb():
            return

        # ----------------------------

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            # if save_original_checkbox.is_checked():
            #     return {
            #         "rule": "save_original",
            #     }
            # name = ds_name_input.get_value()
            # name.strip("'\"").lstrip("'\"")
            # return {
            #     "name": name,
            # }
            return {}

        def _set_settings_from_json(settings: dict):
            # rule = settings.get("rule", None)
            # if rule == "save_original":
            #     save_original_checkbox.check()
            #     ds_name_input.hide()
            # else:
            #     save_original_checkbox.uncheck()
            #     ds_name = settings.get("name", "")
            #     ds_name_input.set_value(ds_name)
            #     ds_name_input.show()
            return

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = create_settings_options(
                lj_description_container,
                lj_description_sidebar_container,
                lj_description_title_preview,
                lj_members_container,
                lj_members_sidebar_container,
                lj_members_preview_container,
                lj_settings_classes_list_edit_container,
                lj_settings_classes_list_widgets_container,
                lj_settings_classes_list_preview,
                lj_settings_tags_list_edit_container,
                lj_settings_tags_list_widgets_container,
                lj_settings_tags_list_preview,
                lj_filters_edit_container,
                lj_filters_condition_selector_field,
                lj_filters_preview_text,
            )
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            need_preview=False,
        )

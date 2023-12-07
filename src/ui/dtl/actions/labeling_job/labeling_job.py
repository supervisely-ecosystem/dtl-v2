import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely import ProjectMeta

from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_layer_docs,
    classes_list_settings_changed_meta,
    set_classes_list_settings_from_json,
    set_classes_list_preview,
    get_classes_list_value,
    tags_list_settings_changed_meta,
    set_tags_list_settings_from_json,
    set_tags_list_preview,
    get_tags_list_value,
)

import src.globals as g

# from src.ui.dtl.actions.labeling_job.layout.job_data import create_job_data_widgets
from src.ui.dtl.actions.labeling_job.layout.job_description import create_job_description_widgets
from src.ui.dtl.actions.labeling_job.layout.job_members import create_job_members_widgets
from src.ui.dtl.actions.labeling_job.layout.job_settings_classes import (
    create_job_settings_classes_widgets,
)
from src.ui.dtl.actions.labeling_job.layout.job_settings_tags import (
    create_job_settings_tags_widgets,
)
from src.ui.dtl.actions.labeling_job.layout.job_filters import create_job_filters_widgets
from src.ui.dtl.actions.labeling_job.layout.node_layout import create_settings_options
from src.ui.dtl.actions.labeling_job.layout.job_output import create_job_output_widgets
import src.ui.dtl.actions.labeling_job.layout.utils as lj_utils


class LabelingJobAction(OutputAction):
    name = "labeling_job"
    title = "Create Labeling Job"
    docs_url = ""
    description = "Creates Labeling Job with given parameters."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        saved_settings = {}

        saved_classes_settings = "default"
        default_classes_settings = "default"

        saved_tags_settings = "default"
        default_tags_settings = "default"

        # DESCRIPTION
        (
            # sidebar
            lj_description_title_input,
            lj_description_description_editor,
            lj_description_readme_editor,
            lj_description_save_btn,
            lj_description_sidebar_container,
            # preview
            lj_description_title_preview,
            # layout
            lj_description_container,
        ) = create_job_description_widgets()

        # DESCRIPTION CBs
        @lj_description_save_btn.click
        def description_save_btn_cb():
            lj_utils.set_lj_name_preview(lj_description_title_input, lj_description_title_preview)
            _save_settings()

        # ----------------------------

        # MEMBERS
        (
            # sidebar
            lj_members_reviewer_selector,
            lj_members_labelers_selector,
            lj_members_save_btn,
            lj_members_sidebar_container,
            # preview
            lj_members_reviewer_preview,
            lj_members_labelers_preview,
            lj_members_preview_container,
            # layout
            lj_members_container,
        ) = create_job_members_widgets()

        # MEMBERS CBs
        @lj_members_save_btn.click
        def members_save_btn_cb():
            lj_utils.set_lj_reviewer_preview(
                lj_members_reviewer_selector, lj_members_reviewer_preview
            )
            lj_utils.set_lj_labelers_preview(
                lj_members_labelers_selector, lj_members_labelers_preview
            )
            _save_settings()
            return

        # ----------------------------

        # CLASSES
        (
            # sidebar
            lj_settings_classes_list_widget,
            lj_settings_classes_list_save_btn,
            lj_settings_classes_list_set_default_btn,
            lj_settings_classes_list_widgets_container,
            # preview
            lj_settings_classes_list_preview,
            # layout
            lj_settings_classes_list_edit_container,
        ) = create_job_settings_classes_widgets()

        # CLASSES CBs
        @lj_settings_classes_list_save_btn.click
        def classes_save_btn_cb():
            _save_classes_list_settings()
            set_classes_list_preview(
                lj_settings_classes_list_widget,
                lj_settings_classes_list_preview,
                saved_classes_settings,
            )
            _save_settings()
            g.updater("metas")

        @lj_settings_classes_list_set_default_btn.click
        def classes_set_default_btn_cb():
            _set_default_classes_list_setting()
            set_classes_list_settings_from_json(
                lj_settings_classes_list_widget, saved_classes_settings
            )
            set_classes_list_preview(
                lj_settings_classes_list_widget,
                lj_settings_classes_list_preview,
                saved_classes_settings,
            )
            _save_settings()
            g.updater("metas")

        # ----------------------------

        # TAGS
        (
            # sidebar
            lj_settings_tags_list_widget,
            lj_settings_tags_list_save_btn,
            lj_settings_tags_list_set_default_btn,
            lj_settings_tags_list_widgets_container,
            # preview
            lj_settings_tags_list_preview,
            # layout
            lj_settings_tags_list_edit_container,
        ) = create_job_settings_tags_widgets()

        # TAGS CBs
        @lj_settings_tags_list_save_btn.click
        def tags_save_btn_cb():
            _save_tags_list_settings()
            set_tags_list_preview(
                lj_settings_tags_list_widget, lj_settings_tags_list_preview, saved_tags_settings
            )
            _save_settings()
            g.updater("metas")

        @lj_settings_tags_list_set_default_btn.click
        def tags_set_default_btn_cb():
            _set_default_tags_list_setting()
            set_tags_list_settings_from_json(lj_settings_tags_list_widget, saved_tags_settings)
            set_tags_list_preview(
                lj_settings_tags_list_widget, lj_settings_tags_list_preview, saved_tags_settings
            )
            _save_settings()
            g.updater("metas")

        # ----------------------------

        # FILTERS
        (
            # sidebar
            lj_filters_objects_limit_per_item_widget,
            lj_filters_objects_limit_checkbox,
            lj_filters_tags_limit_per_item_widget,
            lj_filters_tags_limit_checkbox,
            lj_filters_sidebar_container,
            lj_filters_save_btn,
            # preview
            lj_filters_objects_limit_preview_text,
            lj_filters_tags_limit_preview_text,
            lj_filters_preview_container,
            # layout
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

        @lj_filters_save_btn.click
        def filters_save_btn_cb():
            lj_utils.set_lj_filter_preview(
                lj_filters_objects_limit_checkbox,
                lj_filters_objects_limit_per_item_widget,
                lj_filters_objects_limit_preview_text,
                lj_filters_tags_limit_checkbox,
                lj_filters_tags_limit_per_item_widget,
                lj_filters_tags_limit_preview_text,
            )
            _save_settings()

        # ----------------------------

        # OUTPUT
        (
            # sidebar
            lj_output_project_name_input,
            lj_output_dataset_keep_checkbox,
            lj_output_dataset_name_input,
            lj_output_save_btn,
            lj_output_sidebar_container,
            # preview
            lj_output_project_name_preview,
            lj_output_dataset_name_preview,
            lj_output_container_preview,
            # layout
            lj_output_edit_container,
        ) = create_job_output_widgets()

        # OUTPUT CBs
        @lj_output_save_btn.click
        def dataset_save_btn_cb():
            lj_utils.set_lj_output_project_name_preview(
                lj_output_project_name_input, lj_output_project_name_preview
            )
            lj_utils.set_lj_output_dataset_name_preview(
                lj_output_dataset_name_input,
                lj_output_dataset_keep_checkbox,
                lj_output_dataset_name_preview,
            )
            _save_settings()
            return

        @lj_output_dataset_keep_checkbox.value_changed
        def dataset_keep_checkbox_cb(is_checked):
            if is_checked:
                lj_output_dataset_name_input.hide()
            else:
                lj_output_dataset_name_input.show()

        # ----------------------------

        def _set_default_classes_list_setting():
            nonlocal saved_classes_settings
            saved_classes_settings = copy.deepcopy(default_classes_settings)

        def _set_default_tags_list_setting():
            nonlocal saved_tags_settings
            saved_tags_settings = copy.deepcopy(default_tags_settings)

        def _get_classes_list_value():
            return get_classes_list_value(lj_settings_classes_list_widget, multiple=True)

        def _get_tags_list_value():
            return get_tags_list_value(lj_settings_tags_list_widget, multiple=True)

        def _save_classes_list_settings():
            nonlocal saved_classes_settings
            saved_classes_settings = _get_classes_list_value()

        def _save_tags_list_settings():
            nonlocal saved_tags_settings
            saved_tags_settings = _get_tags_list_value()

        def _set_classes_list_preview():
            set_classes_list_preview(
                lj_settings_classes_list_widget,
                lj_settings_classes_list_preview,
                saved_classes_settings,
            )

        def _set_tags_list_preview():
            set_tags_list_preview(
                lj_settings_tags_list_widget,
                lj_settings_tags_list_preview,
                saved_tags_settings,
            )

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return

            _current_meta = project_meta

            lj_settings_classes_list_widget.loading = True
            lj_settings_tags_list_widget.loading = True

            obj_classes = project_meta.obj_classes
            lj_settings_classes_list_widget.set(obj_classes)

            tag_metas = project_meta.tag_metas
            lj_settings_tags_list_widget.set(tag_metas)

            nonlocal saved_classes_settings
            saved_classes_settings = classes_list_settings_changed_meta(
                saved_classes_settings,
                obj_classes,
            )
            nonlocal saved_tags_settings
            saved_tags_settings = tags_list_settings_changed_meta(
                saved_tags_settings,
                tag_metas,
            )

            set_classes_list_settings_from_json(
                lj_settings_classes_list_widget,
                saved_classes_settings,
            )
            set_tags_list_settings_from_json(
                lj_settings_tags_list_widget,
                saved_tags_settings,
            )

            _set_classes_list_preview()
            _set_tags_list_preview()

            lj_settings_classes_list_widget.loading = False
            lj_settings_tags_list_widget.loading = False
            _save_settings()

        def _save_settings():
            nonlocal saved_settings
            settings = lj_utils.save_settings(
                # lj_dataset_selector,
                lj_description_title_input,
                lj_description_readme_editor,
                lj_description_description_editor,
                lj_members_reviewer_selector,
                lj_members_labelers_selector,
                saved_classes_settings,
                saved_tags_settings,
                lj_filters_objects_limit_checkbox,
                lj_filters_objects_limit_per_item_widget,
                lj_filters_tags_limit_checkbox,
                lj_filters_tags_limit_per_item_widget,
                lj_output_project_name_input,
                lj_output_dataset_keep_checkbox,
                lj_output_dataset_name_input,
            )
            saved_settings = settings

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return saved_settings

        def _set_settings_from_json(settings: dict):
            lj_utils.set_settings_from_json(
                settings,
                lj_description_title_input,
                lj_description_title_preview,
                lj_description_readme_editor,
                lj_description_description_editor,
                lj_members_reviewer_selector,
                lj_members_reviewer_preview,
                lj_members_labelers_selector,
                lj_members_labelers_preview,
                lj_settings_classes_list_widget,
                lj_settings_classes_list_preview,
                lj_settings_tags_list_widget,
                lj_settings_tags_list_preview,
                lj_filters_objects_limit_checkbox,
                lj_filters_objects_limit_per_item_widget,
                lj_filters_tags_limit_checkbox,
                lj_filters_tags_limit_per_item_widget,
                lj_filters_tags_limit_preview_text,
                lj_filters_objects_limit_preview_text,
                lj_output_project_name_input,
                lj_output_dataset_keep_checkbox,
                lj_output_dataset_name_input,
                lj_output_project_name_preview,
                lj_output_dataset_name_preview,
            )
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
                lj_filters_sidebar_container,
                lj_filters_preview_container,
                lj_output_edit_container,
                lj_output_sidebar_container,
                lj_output_container_preview,
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
            meta_changed_cb=meta_changed_cb,
            need_preview=False,
        )

    @classmethod
    def create_outputs(cls):
        return []

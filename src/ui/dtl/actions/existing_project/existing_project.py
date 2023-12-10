from typing import Optional
import json
from os.path import realpath, dirname

import src.globals as g
from supervisely.app.widgets import (
    NodesFlow,
    Text,
    Select,
    SelectProject,
    SelectDataset,
    Button,
    Container,
    Input,
    ProjectThumbnail,
    Field,
    OneOf,
    Empty,
)

from supervisely.app.content import StateJson

from src.ui.dtl.utils import (
    get_layer_docs,
    get_set_settings_button_style,
    get_set_settings_container,
    get_text_font_size,
    create_save_btn,
)
from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size


class ExistingProjectAction(OutputAction):
    name = "existing_project"
    title = "Existing Project"
    docs_url = ""
    description = "Save results of data transformations to existing project in current workspace."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        saved_settings = {}

        # SIDEBAR
        dst_project_selector = SelectProject(
            workspace_id=g.WORKSPACE_ID,
            allowed_types=[g.SUPPORTED_MODALITIES_MAP[g.MODALITY_TYPE]],
            size="small",
        )

        # fix team and workspace for SelectProject widget
        StateJson()[dst_project_selector._ws_selector._team_selector.widget_id][
            "teamId"
        ] = g.TEAM_ID
        StateJson()[dst_project_selector._ws_selector.widget_id]["workspaceId"] = g.WORKSPACE_ID
        dst_project_selector._ws_selector.disable()
        StateJson().send_changes()

        dst_project_selector_field = Field(
            title="Select Project",
            description="Results will be saved to selected project.",
            content=dst_project_selector,
        )

        dst_dataset_options_existing_dataset_selector = SelectDataset(
            compact=True,
            size="small",
            allowed_project_types=[g.SUPPORTED_MODALITIES_MAP[g.MODALITY_TYPE]],
        )
        dst_dataset_options_new_dataset_input = Input(
            placeholder="Enter dataset name", size="small"
        )

        dst_dataset_options_selector_items = [
            Select.Item("new", "New Dataset", dst_dataset_options_new_dataset_input),
            Select.Item(
                "existing", "Existing Dataset", dst_dataset_options_existing_dataset_selector
            ),
            Select.Item("keep", "Keep original dataset from input project", Empty()),
        ]
        dst_dataset_options_selector = Select(dst_dataset_options_selector_items, size="small")
        dst_dataset_options_selector_oneof = OneOf(dst_dataset_options_selector)
        dst_dataset_options_selector_field = Field(
            title="Select Dataset Options",
            description=(
                "Existing Dataset: Select dataset from existing project to save results to. "
                "New Dataset: Enter name of new dataset to create in selected existing project. "
                "Keep original dataset from input project: Keep original dataset from input project."
            ),
            content=Container([dst_dataset_options_selector, dst_dataset_options_selector_oneof]),
        )

        sidebar_save_button = create_save_btn()
        sidebar_container = Container(
            [dst_project_selector_field, dst_dataset_options_selector_field, sidebar_save_button]
        )

        # SIDEBAR CBs
        @dst_project_selector.value_changed
        def on_dst_project_selector_change(project_id):
            dst_dataset_options_existing_dataset_selector.set_project_id(project_id)

        @dst_dataset_options_existing_dataset_selector.value_changed
        def on_dst_dataset_options_existing_dataset_selector_change(dataset_id):
            return

        @sidebar_save_button.click
        def on_save_btn_click():
            _save_settings()

        # -----------------------------

        # LAYOUT
        select_project_text = Text("Select Project", status="text", font_size=get_text_font_size())
        select_project_btn = Button(
            text="SELECT",
            icon="zmdi zmdi-folder",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        select_project_container = get_set_settings_container(
            select_project_text, select_project_btn
        )
        # -----------------------------

        # PREVIEW
        dst_project_preview = ProjectThumbnail()
        dst_dataset_preview = Text("", "text", font_size=get_text_font_size())
        dst_preview_container = Container([dst_project_preview, dst_dataset_preview])
        dst_preview_container.hide()
        # -----------------------------

        def _update_preview():
            project_info = g.api.project.get_info_by_id(dst_project_selector.get_selected_id())
            dst_project_preview.set(project_info)

            dataset_option = dst_dataset_options_selector.get_value()
            if dataset_option == "new":
                dst_dataset_preview.set(
                    f"Dataset: {dst_dataset_options_new_dataset_input.get_value()}", "text"
                )
            elif dataset_option == "existing":
                dataset_name = g.api.dataset.get_info_by_id(
                    dst_dataset_options_existing_dataset_selector.get_selected_id()
                ).name
                dst_dataset_preview.set(f"Dataset: {dataset_name}", "text")
            else:
                dst_dataset_preview.set("Dataset: Keep original dataset from input project", "text")
            dst_preview_container.show()

        def get_settings(options_json: dict):
            nonlocal saved_settings
            return saved_settings

        def _set_settings_from_json(settings: dict):
            project_id = settings.get("project_id", None)
            dst_project_selector.set_project_id(project_id)
            dataset_option = settings.get("dataset_option", "new")
            dst_dataset_options_selector.set_value(dataset_option)
            if dataset_option == "new":
                dataset_name = settings.get("dataset_name", "")
                dst_dataset_options_new_dataset_input.set_value(dataset_name)
            elif dataset_option == "existing":
                dataset_id = settings.get("dataset_id", None)
                dst_dataset_options_existing_dataset_selector.set_dataset_id(dataset_id)
            else:
                pass
            _save_settings()

        def _save_settings():
            nonlocal saved_settings
            settings = {
                "project_id": dst_project_selector.get_selected_id(),
                "dataset_name": None,
                "dataset_id": None,
            }
            dataset_options = dst_dataset_options_selector.get_value()
            if dataset_options == "new":
                settings["dataset_option"] = "new"
                settings["dataset_name"] = dst_dataset_options_new_dataset_input.get_value()
            elif dataset_options == "existing":
                settings["dataset_option"] = "existing"
                settings[
                    "dataset_id"
                ] = dst_dataset_options_existing_dataset_selector.get_selected_id()
            else:
                settings["dataset_option"] = "keep"

            saved_settings = settings
            _update_preview()

        def get_dst(options_json: dict) -> dict:
            project_id = dst_project_selector.get_selected_id()
            if project_id is not None:
                project_name = g.api.project.get_info_by_id(project_id).name
            else:
                project_name = None
            dst = project_name
            if dst is None or dst == "":
                return []
            if dst[0] == "[":
                dst = json.loads(dst)
            else:
                dst = [dst.strip("'\"")]
            return dst

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            dst_options = [
                NodesFlow.Node.Option(
                    name="Select Project",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=select_project_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(sidebar_container),
                        sidebar_width=400,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="classes_mapping_preview",
                    option_component=NodesFlow.WidgetOptionComponent(dst_preview_container),
                ),
            ]
            return {
                "src": [],
                "dst": dst_options,
                "settings": [],
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            get_dst=get_dst,
            need_preview=False,
        )

    @classmethod
    def create_outputs(cls):
        return []

from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import NodesFlow, SelectTagMeta, Container, Button, Text, Select
from supervisely import ProjectMeta, TagMeta, Tag
from supervisely.annotation.tag_meta import TagValueType

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import InputTag, TagMetasPreview
from src.ui.dtl.utils import (
    get_set_settings_button_style,
    get_set_settings_container,
    get_layer_docs,
    create_save_btn,
)


class TagAction(AnnotationAction):
    name = "tag"
    title = "Tag"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/tag"
    description = "Add or remove tags from images."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()

        select_tag_meta = SelectTagMeta(project_meta=_current_meta)
        input_tag = InputTag(TagMeta(name="", value_type=TagValueType.NONE))
        save_tag_btn = create_save_btn()
        input_tag_widgets_container = Container(widgets=[select_tag_meta, input_tag, save_tag_btn])
        tag_preview_meta = TagMetasPreview()
        tag_preview_value = Text("")
        rag_preview_widgets_container = Container(
            widgets=[tag_preview_meta, tag_preview_value], gap=1
        )
        input_tag_edit_text = Text("Classes List")
        input_tag_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        input_tag_edit_container = get_set_settings_container(
            input_tag_edit_text, input_tag_edit_btn
        )

        action_text = Text("Action", status="text")
        action_selector = Select(
            [Select.Item("add", "Add"), Select.Item("delete", "Delete")],
            size="small",
        )

        saved_tag_setting = None

        last_tag_meta = None

        @select_tag_meta.value_changed
        def select_tag_meta_value_changed(tag_meta: TagMeta):
            if last_tag_meta == tag_meta:
                return
            input_tag.loading = True
            input_tag.set_tag_meta(tag_meta)
            input_tag.loading = False

        def _get_tag_value():
            selected_tag = input_tag.get_tag()
            selected_tag: Tag
            if selected_tag is None:
                tag = None
            elif selected_tag.meta.value_type == str(TagValueType.NONE):
                tag = selected_tag.meta.name
            else:
                tag = {
                    "name": selected_tag.meta.name,
                    "value": selected_tag.value,
                }
            return tag

        def _save_tag():
            nonlocal saved_tag_setting
            saved_tag_setting = _get_tag_value()
            tag_preview_value.text = (
                ""
                if isinstance(saved_tag_setting, str) or saved_tag_setting is None
                else str(saved_tag_setting["value"])
            )
            if saved_tag_setting is not None:
                if isinstance(saved_tag_setting, str):
                    tag_name = saved_tag_setting
                else:
                    tag_name = saved_tag_setting["name"]
                tag_meta = select_tag_meta.get_tag_meta_by_name(tag_name)
                tag_preview_meta.set([tag_meta])

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {"tag": saved_tag_setting, "action": action_selector.get_value()}

        def _set_settings_from_json(settings: dict):
            if "tag" not in settings:
                return
            select_tag_meta.loading = True
            input_tag.loading = True
            if isinstance(settings["tag"], str):
                tag_name = settings["tag"]
                tag_value = None
            else:
                tag_name = settings["tag"]["name"]
                tag_value = settings["tag"]["value"]
            tag_meta = select_tag_meta.get_tag_meta_by_name(tag_name)
            select_tag_meta.set_name(tag_name)
            input_tag.set_tag_meta(tag_meta)
            input_tag.value = tag_value
            select_tag_meta.loading = False
            input_tag.loading = False
            _save_tag()

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if _current_meta == project_meta:
                return
            _current_meta = project_meta
            select_tag_meta.loading = True
            current_tag_meta = select_tag_meta.get_selected_item()
            current_tag_value = input_tag.get_value()
            select_tag_meta.set_project_meta(project_meta)

            # to preserve selected tag meta and value
            if current_tag_meta is not None and current_tag_meta.name in [
                tm.name for tm in project_meta.tag_metas
            ]:
                select_tag_meta.set_name(current_tag_meta.name)
                input_tag.set_value(current_tag_value)

            select_tag_meta.loading = False

        save_tag_btn.click(_save_tag)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Input Tag",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=input_tag_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            input_tag_widgets_container
                        ),
                        sidebar_width=340,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="tag_preview",
                    option_component=NodesFlow.WidgetOptionComponent(rag_preview_widgets_container),
                ),
                NodesFlow.Node.Option(
                    name="action_text",
                    option_component=NodesFlow.WidgetOptionComponent(action_text),
                ),
                NodesFlow.Node.Option(
                    name="action_selector",
                    option_component=NodesFlow.WidgetOptionComponent(action_selector),
                ),
            ]
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
        )

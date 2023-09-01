from typing import Optional
from supervisely.app.widgets import NodesFlow, SelectTagMeta, Container
from supervisely import ProjectMeta, TagMeta, Tag
from supervisely.annotation.tag_meta import TagValueType
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import InputTag


class TagAction(Action):
    name = "tag"
    title = "Tag"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/tag"
    description = "Tag layer (tag) adds or removes tags from images. Tags are used for several things, e.g. to split images by folders in save layers or to filter images by tag."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "tag": None,
        "action": "Select Action",
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        prev_project_meta = ProjectMeta()

        select_tag_meta = SelectTagMeta(project_meta=prev_project_meta)
        input_tag = InputTag(TagMeta(name="placeholder", value_type=TagValueType.NONE))

        last_tag_meta = None

        @select_tag_meta.value_changed
        def select_tag_meta_value_changed(tag_meta: TagMeta):
            if last_tag_meta == tag_meta:
                return
            input_tag.loading = True
            input_tag.set_tag_meta(tag_meta)
            input_tag.loading = False

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
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
            return {"tag": tag, "action": options_json["Select Action"]}

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
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
            node_state["action"] = settings["action"]
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal prev_project_meta
            if prev_project_meta == project_meta:
                return
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
            prev_project_meta = project_meta

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="input_tag_text",
                option_component=NodesFlow.TextOptionComponent("Tag"),
            ),
            NodesFlow.Node.Option(
                name="Input Tag",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        Container(widgets=[select_tag_meta, input_tag])
                    )
                ),
            ),
            NodesFlow.Node.Option(
                name="action_text",
                option_component=NodesFlow.TextOptionComponent("Action"),
            ),
            NodesFlow.Node.Option(
                name="Select Action",
                option_component=NodesFlow.SelectOptionComponent(
                    items=[
                        NodesFlow.SelectOptionComponent.Item("add", "Add"),
                        NodesFlow.SelectOptionComponent.Item("delete", "Delete"),
                    ],
                    default_value="add",
                ),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            set_settings_from_json=set_settings_from_json,
            get_src=None,
            meta_changed_cb=meta_changed_cb,
            get_dst=None,
            id=layer_id,
        )

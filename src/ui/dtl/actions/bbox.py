from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesMapping


class BBoxAction(Action):
    name = "bbox"
    title = "Bounding Box"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bbox"
    description = "Bounding Box layer (bbox) converts annotations of specified classes to bounding boxes. Annotations would be replaced with new objects of shape rectangle."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes_mapping": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes_mapping = ClassesMapping()

        def _get_classes_mapping_value():
            mapping = classes_mapping.get_mapping()
            values = {
                name: values["value"]
                for name, values in mapping.items()
                if not values["ignore"] and not values["default"]
            }
            return values

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes_mapping": _get_classes_mapping_value(),
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            classes_mapping.loading = True
            classes_mapping.set_mapping(settings["classes_mapping"])
            classes_mapping.loading = False
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            classes_mapping.loading = True
            classes_mapping.set(project_meta.obj_classes)
            classes_mapping.loading = False

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Classes Mapping"),
            ),
            NodesFlow.Node.Option(
                name="Set Classes Mapping",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_mapping)
                ),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=meta_changed_cb,
            get_dst=None,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

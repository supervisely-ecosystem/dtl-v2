from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesColorMapping
from supervisely.imaging.color import hex2rgb


class ColorClassAction(Action):
    name = "color_class"
    title = "Color Class"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/color_class"
    )
    description = "This layer (color_class) used for coloring classes as you wish. Add this class at the end of graph, before data saving."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes_color_mapping": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes_colors = ClassesColorMapping()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes_color_mapping": {
                    cls_name: hex2rgb(value["value"])
                    for cls_name, value in classes_colors.get_mapping().items()
                }
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            classes_colors.loading = True
            classes_colors.set_colors(
                [
                    settings.get(cls, hex2rgb(value["value"]))
                    for cls, value in classes_colors.get_mapping().items()
                ]
            )
            classes_colors.loading = False
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            classes_colors.loading = True
            classes_colors.set(project_meta.obj_classes)
            classes_colors.loading = False

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="classes_colors_text",
                option_component=NodesFlow.TextOptionComponent("Classes Colors"),
            ),
            NodesFlow.Node.Option(
                name="Set Colors",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_colors)
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

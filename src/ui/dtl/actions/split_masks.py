from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from supervisely import Bitmap, AnyGeometry
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class SplitMasksAction(Action):
    name = "split_masks"
    title = "Split Masks"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/split_masks"
    )
    description = "This layer (split_masks) takes one bitmap annotation and split it into few bitmap masks if it contain non-connected components."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes = ClassesList(multiple=True)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": [cls.name for cls in classes.get_selected_classes()],
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            classes.loading = True
            classes.select(settings["classes"])
            classes.loading = False
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            classes.loading = True
            classes.set(
                [
                    cls
                    for cls in project_meta.obj_classes
                    if cls.geometry_type in [Bitmap, AnyGeometry]
                ]
            )
            classes.loading = False

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes"),
            ),
            NodesFlow.Node.Option(
                name="Select Classes",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes)
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

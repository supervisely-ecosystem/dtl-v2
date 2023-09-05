from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from supervisely import Bitmap, AnyGeometry
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class MergeBitmapsAction(Action):
    name = "merge_bitmap_masks"
    title = "Merge Masks"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/merge_masks"
    )
    description = "This layer (merge_bitmap_masks) takes all bitmap annotations which has same class name and merge it into single bitmap annotation."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "class": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes = ClassesList(multiple=False)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            try:
                class_name = classes.get_selected_classes()[0].name
            except:
                class_name = None
            return {
                "class": class_name,
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = [settings["class"]]
            classes.loading = True
            classes.select(obj_class_names)
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
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
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

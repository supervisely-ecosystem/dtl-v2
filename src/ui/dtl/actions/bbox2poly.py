from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta, Rectangle, AnyGeometry
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesMapping


class BboxToPolyAction(Action):
    name = "bbox2poly"
    title = "BBox to Polygon"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bbox2poly"
    )
    description = 'This layer (bbox2poly) converts rectangles ("bounding boxes") to polygons.'
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes_mapping": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes_mapping_widget = ClassesMapping()

        def _get_classes_mapping_value():
            mapping = classes_mapping_widget.get_mapping()
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

        def meta_changed_cb(project_meta: ProjectMeta):
            classes_mapping_widget.loading = True
            classes_mapping_widget.set(
                [
                    cls
                    for cls in project_meta.obj_classes
                    if cls.geometry_type in [Rectangle, AnyGeometry]
                ]
            )
            classes_mapping_widget.loading = False

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            classes_mapping_widget.loading = True
            settings = json_data["settings"]
            classes_mapping = {}
            other_default = settings["classes_mapping"].get("__other__", None) == "__default__"
            for cls in classes_mapping_widget.get_classes():
                if cls.name in settings["classes_mapping"]:
                    value = settings["classes_mapping"][cls.name]
                    if value == "__default__":
                        value = cls.name
                    if value == "__ignore__":
                        value = ""
                    classes_mapping[cls.name] = value
                elif other_default:
                    classes_mapping[cls.name] = cls.name
                else:
                    classes_mapping[cls.name] = ""
            classes_mapping_widget.set_mapping(classes_mapping)
            classes_mapping_widget.loading = False
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="class_text",
                option_component=NodesFlow.TextOptionComponent("Class"),
            ),
            NodesFlow.Node.Option(
                name="Set Classes",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_mapping_widget)
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

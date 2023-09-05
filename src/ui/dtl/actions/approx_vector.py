from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from supervisely import Polygon, Polyline, AnyGeometry
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class ApproxVectorAction(Action):
    name = "approx_vector"
    title = "Approx Vector"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/approx_vector"
    )
    description = "This layer (approx_vector) approximates vector figures: lines and polygons. The operation decreases number of vertices with Douglas-Peucker algorithm."
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
                "classes": [obj_class.name for obj_class in classes.get_selected_classes()],
                "epsilon": options_json["epsilon"],
            }

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = settings["classes"]
            classes.loading = True
            classes.select(obj_class_names)
            classes.loading = False
            node_state["epsilon"] = settings["epsilon"]
            return node_state

        def meta_changed_cb(project_meta: ProjectMeta):
            classes.loading = True
            classes.set(
                [
                    cls
                    for cls in project_meta.obj_classes
                    if cls.geometry_type in [Polygon, Polyline, AnyGeometry]
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
            NodesFlow.Node.Option(
                name="epsilon_text",
                option_component=NodesFlow.TextOptionComponent("Epsilon"),
            ),
            NodesFlow.Node.Option(
                name="epsilon",
                option_component=NodesFlow.IntegerOptionComponent(min=1, default_value=3),
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

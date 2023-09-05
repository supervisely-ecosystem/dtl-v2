from typing import Optional
from src.ui.dtl.Action import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta, Bitmap, AnyGeometry


class SkeletonizeAction(Action):
    name = "skeletonize"
    title = "Skeletonize"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/skeletonize"
    )
    description = "This layer (skeletonize) extracts skeletons from bitmap figures."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        classes_widget = ClassesList(multiple=True)
        _current_meta = ProjectMeta()

        methods = [
            ("skeletonization", "Skeletonization"),
            ("medial_axis", "Medial axis"),
            ("thinning", "Thinning"),
        ]
        items = [NodesFlow.SelectOptionComponent.Item(*method) for method in methods]

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": [cls.name for cls in classes_widget.get_selected_classes()],
                "method": options_json["method"],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta.obj_classes != _current_meta.obj_classes:
                classes_widget.loading = True
                classes_widget.set(
                    [
                        cls
                        for cls in project_meta.obj_classes
                        if cls.geometry_type in [Bitmap, AnyGeometry]
                    ]
                )
                classes_widget.loading = False
            _current_meta = project_meta

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = settings["classes"]
            classes_widget.loading = True
            classes_widget.select(obj_class_names)
            classes_widget.loading = False
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes"),
            ),
            NodesFlow.Node.Option(
                name="Select Classes",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_widget)
                ),
            ),
            NodesFlow.Node.Option(
                name="method_text",
                option_component=NodesFlow.TextOptionComponent("Method"),
            ),
            NodesFlow.Node.Option(
                name="method",
                option_component=NodesFlow.SelectOptionComponent(
                    items=items, default_value=items[0].value
                ),
            ),
        ]

        return Layer(
            action=cls,
            id=layer_id,
            options=options,
            get_src=None,
            get_dst=None,
            get_settings=get_settings,
            meta_changed_cb=meta_changed_cb,
            set_settings_from_json=set_settings_from_json,
        )

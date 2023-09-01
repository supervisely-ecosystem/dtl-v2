from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta, Polyline, AnyGeometry


class DropLinesByLengthAction(Action):
    name = "drop_lines_by_length"
    title = "Drop Lines by Length"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/drop_lines_by_length"
    description = "Layer drop_lines_by_length - remove too long or to short lines. Also this layer can drop lines with length in range. Lines with more than two points also supported. For multi-lines total length is calculated as sum of sections."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "lines_class": None,
        "resolution_compensation": "Resolution Compensation",
        "invert": "Invert",
        "min_length": None,
        "max_length": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes = ClassesList(multiple=False)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            try:
                lines_class = classes.get_selected_classes()[0].name
            except:
                lines_class = ""
            return {
                "lines_class": lines_class,
                "resolution_compensation": bool(options_json["Resolution Compensation"]),
                "invert": bool(options_json["Invert"]),
                "min_length": options_json["min_length"] if options_json["Min Length"] else 0,
                "max_length": options_json["max_length"] if options_json["Max Length"] else 0,
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta.obj_classes != _current_meta.obj_classes:
                classes.loading = True
                classes.set(
                    [
                        cls
                        for cls in project_meta.obj_classes
                        if cls.geometry_type in [Polyline, AnyGeometry]
                    ]
                )
                classes.loading = False
            _current_meta = project_meta

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = [settings["lines_class"]]
            classes.loading = True
            classes.select(obj_class_names)
            classes.loading = False
            min_length = settings["min_length"]
            node_state["min_length"] = min_length if min_length is not None else 1
            node_state["Min Length"] = min_length is not None
            max_length = settings["max_length"]
            node_state["max_length"] = max_length if max_length is not None else 1
            node_state["Max Length"] = max_length is not None
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Line Class"),
            ),
            NodesFlow.Node.Option(
                name="Select Classes",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes)
                ),
            ),
            NodesFlow.Node.Option(
                name="Resolution Compensation",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=False),
            ),
            NodesFlow.Node.Option(
                name="Invert",
                option_component=NodesFlow.CheckboxOptionComponent(default_value=False),
            ),
            NodesFlow.Node.Option(
                name="Min Length",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="min_length",
                option_component=NodesFlow.IntegerOptionComponent(min=0, default_value=1),
            ),
            NodesFlow.Node.Option(
                name="Max Length",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="max_length",
                option_component=NodesFlow.IntegerOptionComponent(min=0, default_value=1),
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

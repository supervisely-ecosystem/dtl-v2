from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta


class DropByClassAction(Action):
    name = "drop_obj_by_class"
    title = "Drop by Class"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/drop_obj_by_class"
    description = "This layer (drop_obj_by_class) simply removes annotations of specified classes. You can also use data layer and map unnecessary classes to __ignore__."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes = ClassesList(multiple=True)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": [obj_class.name for obj_class in classes.get_selected_classes()],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta.obj_classes != _current_meta.obj_classes:
                classes.loading = True
                classes.set(project_meta.obj_classes)
                classes.loading = False
            _current_meta = project_meta

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = settings["classes"]
            classes.loading = True
            classes.select(obj_class_names)
            classes.loading = False
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
            get_src=None,
            meta_changed_cb=meta_changed_cb,
            get_dst=None,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

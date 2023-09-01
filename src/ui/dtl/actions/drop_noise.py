from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList
from supervisely.app.widgets import NodesFlow, Switch, InputNumber, OneOf, Flexbox
from supervisely import ProjectMeta, Bitmap, AnyGeometry


class DropNoiseAction(Action):
    name = "drop_noise"
    title = "Drop Noise"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/drop_noise_from_bitmap"
    description = "This layer (drop_noise) removes connected components smaller than the specified size from bitmap annotations. This can be useful to eliminate noise after running neural network."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "classes": None,
        "min_area": None,
        "src_type": "Source type",
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes = ClassesList(multiple=False)
        input_px = InputNumber(min=0)
        input_percent = InputNumber(min=0, max=100)
        px_or_percent_switch = Switch(
            switched=True,
            on_text="px",
            off_text="%",
            off_color="#20a0ff",
            on_content=input_px,
            off_content=input_percent,
        )
        input_value = OneOf(px_or_percent_switch)
        min_area_widgets = Flexbox(widgets=[input_value, px_or_percent_switch])

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes": [cls.name for cls in classes.get_selected_classes()],
                "min_area": _get_min_area(),
                "src_type": options_json["Source type"],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta.obj_classes != _current_meta.obj_classes:
                classes.loading = True
                classes.set(
                    [
                        cls
                        for cls in project_meta.obj_classes
                        if cls.geometry_type in [Bitmap, AnyGeometry]
                    ]
                )
                classes.loading = False
            _current_meta = project_meta

        def _get_min_area():
            if px_or_percent_switch.is_switched():
                return f"{input_px.value}px"
            else:
                return f"{input_percent.value}%"

        def _set_min_area(value):
            if value.endswith("px"):
                px_or_percent_switch.on()
                input_px.value = int(value[:-2])
            else:
                px_or_percent_switch.off()
                input_percent.value = int(value[:-1])

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            obj_class_names = settings["classes"]
            classes.loading = True
            classes.select(obj_class_names)
            classes.loading = False
            min_area_widgets.loading = True
            _set_min_area(settings["min_area"])
            min_area_widgets.loading = False
            return node_state

        src_type_option_items = [
            NodesFlow.SelectOptionComponent.Item("image", "Image"),
            NodesFlow.SelectOptionComponent.Item("bbox", "Bounding Box"),
        ]
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
            NodesFlow.Node.Option(
                name="Min Area",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(min_area_widgets)
                ),
            ),
            NodesFlow.Node.Option(
                name="Source type",
                option_component=NodesFlow.SelectOptionComponent(
                    items=src_type_option_items, default_value="image"
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

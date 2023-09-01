from typing import Optional
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from supervisely import ProjectMeta
from supervisely.app.widgets import NodesFlow, Select, Container, InputNumber, Field, OneOf
from src.ui.widgets import ClassesList


class ObjectsFilterAction(Action):
    name = "objects_filter"
    title = "Objects Filter"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/objects_filter"
    )
    description = "This layer (objects_filter) deletes annotations less (or greater) than specified size or percentage of image area."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "filter_by": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        classes = ClassesList(multiple=True)
        percent_input = InputNumber(min=0, max=100, value=5)
        width_input = InputNumber(min=0, value=100)
        height_input = InputNumber(min=0, value=100)
        size_input = Container(
            widgets=[
                Field(title="Width", content=width_input),
                Field(title="Height", content=height_input),
            ]
        )
        comparator_select = Select(
            items=[Select.Item("less", "Less"), Select.Item("greater", "Greater")]
        )
        action_select = Select(items=[Select.Item("delete", "Delete")])
        action_select.disable()
        filter_items = [
            Select.Item("names", "Names", classes),
            Select.Item(
                "area_percent",
                "Area percent",
                Container(widgets=[classes, percent_input, comparator_select, action_select]),
            ),
            Select.Item(
                "bbox_size",
                "Bounding box size",
                Container(widgets=[classes, size_input, comparator_select, action_select]),
            ),
        ]
        filter_by_select = Select(filter_items)
        filter_by_inputs = OneOf(filter_by_select)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            settings = {}
            filter_by = filter_by_select.get_value()
            if filter_by == "names":
                settings["filter_by"] = {
                    "names": [cls.name for cls in classes.get_selected_classes()],
                }
                return settings
            settings["filter_by"] = {
                "polygon_sizes": {
                    "filtering_classes": [cls.name for cls in classes.get_selected_classes()],
                    "action": action_select.get_value(),
                    "comparator": comparator_select.get_value(),
                },
            }
            if filter_by == "area_percent":
                settings["filter_by"]["polygon_sizes"]["area_size"] = {
                    "percent": percent_input.get_value(),
                }
            elif filter_by == "bbox_size":
                settings["filter_by"]["polygon_sizes"]["area_size"] = {
                    "width": width_input.get_value(),
                    "height": height_input.get_value(),
                }
            return settings

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            if "names" in settings["filter_by"]:
                classes.loading = True
                filter_by_select.loading = True
                filter_by_select.set_value("names")
                classes.select(settings["filter_by"]["names"])
                filter_by_select.loading = False
                classes.loading = False
            else:
                filter_by_select.loading = True
                classes.loading = True
                comparator_select.loading = True

                if "percent" in settings["filter_by"]["polygon_sizes"]["area_size"]:
                    percent_input.loading = True
                    filter_by_select.set_value("area_percent")
                    percent_input.value = settings["filter_by"]["polygon_sizes"]["area_size"][
                        "percent"
                    ]
                else:
                    size_input.loading = True
                    filter_by_select.set_value("bbox_size")
                    width_input.value = settings["filter_by"]["polygon_sizes"]["area_size"]["width"]
                    height_input.value = settings["filter_by"]["polygon_sizes"]["area_size"][
                        "height"
                    ]
                classes.select(settings["filter_by"]["polygon_sizes"]["filtering_classes"])
                comparator_select.set_value(settings["filter_by"]["polygon_sizes"]["comparator"])

                filter_by_select.loading = False
                size_input.loading = False
                percent_input.loading = False
                classes.loading = False
                comparator_select.loading = False
            return node_state

        prev_project_meta = ProjectMeta()

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal prev_project_meta
            if prev_project_meta == project_meta:
                return
            classes.loading = True
            classes.set(project_meta.obj_classes)
            classes.loading = False
            prev_project_meta = project_meta

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="filter_by_text",
                option_component=NodesFlow.TextOptionComponent("Objects Filter settings:"),
            ),
            NodesFlow.Node.Option(
                name="Set Filter",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(
                        Container(widgets=[filter_by_select, filter_by_inputs])
                    )
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
            set_settings_from_json=None,
            id=layer_id,
        )

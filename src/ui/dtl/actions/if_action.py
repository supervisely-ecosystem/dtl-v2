from typing import Optional
from supervisely.app.widgets import (
    NodesFlow,
    Select,
    InputNumber,
    SelectTagMeta,
    Container,
    Field,
    Input,
    OneOf,
)
from supervisely import ProjectMeta
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class IfAction(Action):
    name = "if"
    title = "If"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/transformation-layers/if"
    description = (
        "This layer (if) is used to split input data to several flows with a specified criterion."
    )
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "condition": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        class Condition:
            def __init__(self, name, title, widget, get_func, set_func):
                self.name = name
                self.title = title
                self.widget = widget
                self.get_func = get_func
                self.set_func = set_func

            def item(self):
                return Select.Item(self.name, self.title, self.widget)

            def get(self):
                return self.get_func()

            def set(self, value):
                self.set_func(value)
                select_condition.set_value(self.name)

        # probabilty
        _prob_input = InputNumber(min=0, max=100, precision=3)
        _probability_condition_widget = Field(
            title="Probability",
            description="Input probability in percents",
            content=_prob_input,
        )

        def _get_prob_value():
            return _prob_input.get_value() / 100

        def _set_prob_value(condition_json):
            _prob_input.value = condition_json["probability"] * 100

        probability_condition = Condition(
            name="probability",
            title="Probability",
            widget=_probability_condition_widget,
            get_func=_get_prob_value,
            set_func=_set_prob_value,
        )

        # min objects count
        _min_objects_count_input = InputNumber(min=0, max=None)
        _min_objects_count_condition_widget = Field(
            title="Min objects count",
            description="Input min objects count",
            content=_min_objects_count_input,
        )

        def _set_min_obj_count_value(condition_json):
            _min_objects_count_input.value = condition_json["min_objects_count"]

        min_objects_count_condition = Condition(
            name="min_objects_count",
            title="Min objects count",
            widget=_min_objects_count_condition_widget,
            get_func=_min_objects_count_input.get_value,
            set_func=_set_min_obj_count_value,
        )

        # min height
        _min_height_input = InputNumber(min=0, max=None)
        _min_height_condition_widget = Field(
            title="Min height",
            description="Input min height",
            content=_min_height_input,
        )

        def _set_min_height_value(condition_json):
            _min_height_input.value = condition_json["min_height"]

        min_height_condition = Condition(
            name="min_height",
            title="Min height",
            widget=_min_height_condition_widget,
            get_func=_min_height_input.get_value,
            set_func=_set_min_height_value,
        )

        # tags
        _select_tags_input = SelectTagMeta(project_meta=ProjectMeta(), multiselect=True)
        _select_tags_widget = Field(
            title="Tags",
            description="Select tags",
            content=_select_tags_input,
        )

        def _set_tags_value(condition_json):
            _select_tags_input.set_names(condition_json["tags"])

        select_tags_condition = Condition(
            name="tags",
            title="Tags",
            widget=_select_tags_widget,
            get_func=lambda: [tm.name for tm in _select_tags_input.get_selected_items()],
            set_func=_set_tags_value,
        )

        # include classes
        _include_classes_input = ClassesList(multiple=True)
        _include_classes_widget = Field(
            title="Include classes",
            description="Select classes",
            content=_include_classes_input,
        )

        def _set_include_classes_value(condition_json):
            _include_classes_input.select(condition_json["include_classes"])

        select_classes_condition = Condition(
            name="include_classes",
            title="Include classes",
            widget=_include_classes_widget,
            get_func=lambda: [oc.name for oc in _include_classes_input.get_selected_classes()],
            set_func=_set_include_classes_value,
        )

        # name in range
        _names_in_range_inputs = {
            "name_from": Input(),
            "name_to": Input(),
            "step": InputNumber(value=1, min=1, max=None),
        }
        _names_in_range_widget = Field(
            title="Name in range",
            description="Input name in range",
            content=Container(
                widgets=[
                    Field(title="Name from", content=_names_in_range_inputs["name_from"]),
                    Field(title="Name to", content=_names_in_range_inputs["name_to"]),
                    Field(title="Step", content=_names_in_range_inputs["step"]),
                ]
            ),
        )

        def _set_names_in_range_value(condition_json):
            name_from, name_to = condition_json["name_in_range"]
            _names_in_range_inputs["name_from"].set_value(name_from)
            _names_in_range_inputs["name_to"].set_value(name_to)
            _names_in_range_inputs["step"].value = condition_json["frame_step"]

        names_in_range_condition = Condition(
            name="name_in_range",
            title="Name in range",
            widget=_names_in_range_widget,
            get_func=lambda: {
                "name_in_range": [
                    _names_in_range_inputs["name_from"].get_value(),
                    _names_in_range_inputs["name_to"].get_value(),
                ],
                "frame_step": _names_in_range_inputs["step"].get_value(),
            },
            set_func=_set_names_in_range_value,
        )

        conditions = {
            condition.name: condition
            for condition in [
                probability_condition,
                min_objects_count_condition,
                min_height_condition,
                select_tags_condition,
                select_classes_condition,
                names_in_range_condition,
            ]
        }

        select_condition_items = [condition.item() for condition in conditions.values()]
        select_condition = Select(items=select_condition_items)
        condition_input = OneOf(select_condition)
        widget = Container(
            widgets=[
                Field(title="Condition", content=select_condition),
                Field(title="Condition value", content=condition_input),
            ]
        )

        def _get_condition_value(condition_name: str):
            condition = conditions[condition_name]
            return condition.get()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            condition_name = select_condition.get_value()
            condition_value = _get_condition_value(condition_name)
            return {
                "condition": {condition_name: condition_value},
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            _include_classes_input.loading = True
            _select_tags_input.loading = True
            _include_classes_input.set(project_meta.obj_classes)
            # _select_tags_input.set(project_meta=project_meta) # TODO: Add set() method to SelectTagMeta widget in SDK
            _include_classes_input.loading = False
            _select_tags_input.loading = False

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            condition_json = json_data["settings"]["condition"]
            condition_name, _ = list(json_data["settings"]["condition"].items())[0]
            condition = conditions[condition_name]
            condition.set(condition_json)
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="condition_text",
                option_component=NodesFlow.TextOptionComponent("Condition"),
            ),
            NodesFlow.Node.Option(
                name="condition",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(widget)
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

    @classmethod
    def create_outputs(cls):
        return [
            NodesFlow.Node.Output("destination_true", "Destination True"),
            NodesFlow.Node.Output("destination_false", "Destination False"),
        ]

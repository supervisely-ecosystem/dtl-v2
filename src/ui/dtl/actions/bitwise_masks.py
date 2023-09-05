from typing import Optional
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList


class BitwiseMasksAction(Action):
    name = "bitwise_masks"
    title = "Bitwise Masks"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bitwise_masks"
    )
    description = "Bitwise Masks - make bitwise operations between bitmap annotations."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "class_mask": None,
        "classes_to_correct": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        class_mask_widget = ClassesList()
        classes_to_correct_widget = ClassesList(multiple=True)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            try:
                class_mask = class_mask_widget.get_selected_classes()[0].name
            except:
                class_mask = ""
            return {
                "type": options_json["type"],
                "class_mask": class_mask,
                "classes_to_correct": [
                    cls.name for cls in classes_to_correct_widget.get_selected_classes()
                ],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            class_mask_widget.loading = True
            classes_to_correct_widget.loading = True
            class_mask_widget.set(project_meta.obj_classes)
            classes_to_correct_widget.set(project_meta.obj_classes)
            class_mask_widget.loading = False
            classes_to_correct_widget.loading = False

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            class_mask_widget.loading = True
            classes_to_correct_widget.loading = True
            class_mask_widget.select([settings["class_mask"]])
            classes_to_correct_widget.select(settings["classes_to_correct"])
            class_mask_widget.loading = False
            classes_to_correct_widget.loading = False
            return node_state

        type_items = [NodesFlow.SelectOptionComponent.Item(t, t) for t in ("nor", "and", "or")]

        options = [
            NodesFlow.Node.Option(
                name="settings_text",
                option_component=NodesFlow.TextOptionComponent("Settings"),
            ),
            NodesFlow.Node.Option(
                name="type_text",
                option_component=NodesFlow.TextOptionComponent("Operation type"),
            ),
            NodesFlow.Node.Option(
                name="type",
                option_component=NodesFlow.SelectOptionComponent(
                    items=type_items, default_value=type_items[0].value
                ),
            ),
            NodesFlow.Node.Option(
                name="class_mask_text",
                option_component=NodesFlow.TextOptionComponent(
                    "Class Mask. First element of bitwise operation"
                ),
            ),
            NodesFlow.Node.Option(
                name="Select Class Mask",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(class_mask_widget)
                ),
            ),
            NodesFlow.Node.Option(
                name="classes_text",
                option_component=NodesFlow.TextOptionComponent("Classes to correct"),
            ),
            NodesFlow.Node.Option(
                name="Select Classes to correct",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(classes_to_correct_widget)
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

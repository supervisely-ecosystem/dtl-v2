from typing import Optional
import json
from supervisely.app.widgets import NodesFlow
from supervisely import ProjectMeta
from src.ui.dtl import Action
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesColorMapping
from supervisely.imaging.color import hex2rgb


class SaveMasksAction(Action):
    name = "save_masks"
    title = "Save Masks"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/save_masks"
    description = "Save masks layer (save_masks) gives you an opportunity to get masked representations of data besides just images and annotations that you can get using save layer. It includes machine and human representations. In machine masks each of listed classes are colored in shades of gray that you specify. Note that black color [0, 0, 0] is automatically assigned with the background. In human masks you would get stacked original images with that images having class colors above."
    # when setting options from settings json, values from _settings_mapping will be mapped to options.
    # If there is no option mapped directly to setting, set this option mapping to None and set the option value
    # in set_settings_from_json function. If option name is different from setting name - set mapping in
    # _settings_mapping below. If option name is the same as setting name - no need to set mapping.
    _settings_mapping = {
        "masks_human": "Add human masks",
        "masks_machine": "Add machine masks",
        "gt_human_color": None,
        "gt_machine_color": None,
    }

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        human_classes_colors = ClassesColorMapping()
        machine_classes_colors = ClassesColorMapping()

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            masks_human = options_json["Add human masks"]
            gt_human_color = {}
            if masks_human:
                gt_human_color = {
                    cls_name: hex2rgb(value["value"])
                    for cls_name, value in human_classes_colors.get_mapping().items()
                }

            masks_machine = options_json["Add machine masks"]
            gt_machine_color = {}
            if masks_machine:
                gt_machine_color = {
                    cls_name: hex2rgb(value["value"])
                    for cls_name, value in machine_classes_colors.get_mapping().items()
                }

            return {
                "masks_human": masks_human,
                "masks_machine": masks_machine,
                "gt_human_color": gt_human_color,
                "gt_machine_color": gt_machine_color,
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            human_classes_colors.loading = True
            machine_classes_colors.loading = True
            human_classes_colors.set(project_meta.obj_classes)
            machine_classes_colors.set(project_meta.obj_classes)
            human_classes_colors.loading = False
            machine_classes_colors.loading = False

        def get_dst(options_json: dict) -> dict:
            dst = options_json.get("dst", None)
            if dst is None or dst == "":
                return []
            if dst[0] == "[":
                dst = json.loads(dst)
            else:
                dst = [dst.strip("'\"")]
            return dst

        def set_settings_from_json(json_data: dict, node_state: dict):
            """This function is used to set options from settings we get from dlt json input"""
            settings = json_data["settings"]
            human_colors = settings["gt_human_color"]
            current_colors_mapping = human_classes_colors.get_mapping()
            human_classes_colors.set_colors(
                [
                    human_colors.get(cls, hex2rgb(hex_color))
                    for cls, hex_color in current_colors_mapping.items()
                ]
            )
            machine_colors = settings["gt_machine_color"]
            current_colors_mapping = machine_classes_colors.get_mapping()
            machine_classes_colors.set_colors(
                [
                    machine_colors.get(cls, hex2rgb(hex_color))
                    for cls, hex_color in current_colors_mapping.items()
                ]
            )
            return node_state

        options = [
            NodesFlow.Node.Option(
                name="Info",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(cls.create_info_widget())
                ),
            ),
            NodesFlow.Node.Option(
                name="destination_text",
                option_component=NodesFlow.TextOptionComponent("Destination"),
            ),
            NodesFlow.Node.Option(name="dst", option_component=NodesFlow.InputOptionComponent()),
            NodesFlow.Node.Option(
                name="gt_human_color_text",
                option_component=NodesFlow.TextOptionComponent("Human masks colors"),
            ),
            NodesFlow.Node.Option(
                name="Add human masks",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="Set human masks colors",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(human_classes_colors)
                ),
            ),
            NodesFlow.Node.Option(
                name="gt_machine_color_text",
                option_component=NodesFlow.TextOptionComponent("Machine masks colors"),
            ),
            NodesFlow.Node.Option(
                name="Add machine masks",
                option_component=NodesFlow.CheckboxOptionComponent(),
            ),
            NodesFlow.Node.Option(
                name="Set machine masks colors",
                option_component=NodesFlow.ButtonOptionComponent(
                    sidebar_component=NodesFlow.WidgetOptionComponent(machine_classes_colors)
                ),
            ),
        ]

        return Layer(
            action=cls,
            options=options,
            get_settings=get_settings,
            get_src=None,
            meta_changed_cb=meta_changed_cb,
            get_dst=get_dst,
            set_settings_from_json=set_settings_from_json,
            id=layer_id,
        )

    @classmethod
    def create_outputs(cls):
        return []

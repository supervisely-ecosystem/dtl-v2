from typing import Optional
import json

from supervisely.app.widgets import NodesFlow, Button, Container, Text
from supervisely import ProjectMeta
from supervisely.imaging.color import hex2rgb, rgb2hex

from src.ui.dtl import OutputAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesColorMapping, ClassesMappingPreview
from src.ui.dtl.utils import get_set_settings_button_style, get_set_settings_container, get_layer_docs


class SaveMasksAction(OutputAction):
    name = "save_masks"
    title = "Save Masks"
    docs_url = "https://docs.supervisely.com/data-manipulation/index/save-layers/save_masks"
    description = "Export annotations, masks and images to Team Files."
    md_description = get_layer_docs()

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None) -> Layer:
        _current_meta = ProjectMeta()
        human_classes_colors = ClassesColorMapping()
        machine_classes_colors = ClassesColorMapping()
        human_classes_colors_preview = ClassesMappingPreview()
        machine_classes_colors_preview = ClassesMappingPreview()

        human_classes_colors_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        machine_classes_colors_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        human_masks_widgets_container = Container(
            widgets=[human_classes_colors, human_classes_colors_save_btn]
        )
        machine_masks_widgets_container = Container(
            widgets=[machine_classes_colors, machine_classes_colors_save_btn]
        )
        human_masks_edit_text = Text("Human Masks")
        human_masks_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        human_masks_edit_container = get_set_settings_container(
            human_masks_edit_text, human_masks_edit_btn
        )
        machine_masks_edit_text = Text("Machine Masks")
        machine_masks_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        machine_masks_edit_container = get_set_settings_container(
            machine_masks_edit_text, machine_masks_edit_btn
        )

        saved_human_classes_colors_settings = {}
        saved_machine_classes_colors_settings = {}

        def _get_human_classes_colors_value():
            mapping = human_classes_colors.get_mapping()
            values = {
                name: values["value"] for name, values in mapping.items() if not values["ignore"]
            }
            return values

        def _get_machine_classes_colors_value():
            mapping = machine_classes_colors.get_mapping()
            values = {
                name: values["value"] for name, values in mapping.items() if not values["ignore"]
            }
            return values

        def _save_human_classes_colors():
            nonlocal saved_human_classes_colors_settings
            saved_human_classes_colors_settings = {
                cls_name: hex2rgb(value)
                for cls_name, value in _get_human_classes_colors_value().items()
            }
            human_classes_colors_preview.set_mapping(
                {
                    cls_name: rgb2hex(color)
                    for cls_name, color in saved_human_classes_colors_settings.items()
                }
            )

        def _save_machine_classes_colors():
            nonlocal saved_machine_classes_colors_settings
            saved_machine_classes_colors_settings = {
                cls_name: hex2rgb(value)
                for cls_name, value in _get_machine_classes_colors_value().items()
            }
            machine_classes_colors_preview.set_mapping(
                {
                    cls_name: rgb2hex(color)
                    for cls_name, color in saved_machine_classes_colors_settings.items()
                }
            )

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            masks_human = options_json["Add human masks"]
            gt_human_color = {}
            if masks_human:
                gt_human_color = saved_human_classes_colors_settings

            masks_machine = options_json["Add machine masks"]
            gt_machine_color = {}
            if masks_machine:
                gt_machine_color = saved_machine_classes_colors_settings

            return {
                "masks_human": masks_human,
                "masks_machine": masks_machine,
                "gt_human_color": gt_human_color,
                "gt_machine_color": gt_machine_color,
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
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

        def _set_settings_from_json(settings):
            if "gt_human_color" in settings:
                human_colors = settings["gt_human_color"]
                current_colors_mapping = human_classes_colors.get_mapping()
                human_classes_colors.set_colors(
                    [
                        human_colors.get(cls, hex2rgb(hex_color))
                        for cls, hex_color in current_colors_mapping.items()
                    ]
                )
                _save_human_classes_colors()
            if "gt_machine_color" in settings:
                machine_colors = settings["gt_machine_color"]
                current_colors_mapping = machine_classes_colors.get_mapping()
                machine_classes_colors.set_colors(
                    [
                        machine_colors.get(cls, hex2rgb(hex_color))
                        for cls, hex_color in current_colors_mapping.items()
                    ]
                )
                _save_machine_classes_colors()

        human_classes_colors_save_btn.click(_save_human_classes_colors)
        machine_classes_colors_save_btn.click(_save_machine_classes_colors)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            try:
                dst_value = dst[0]
            except IndexError:
                dst_value = ""
            dst_options = [
                NodesFlow.Node.Option(
                    name="destination_text",
                    option_component=NodesFlow.TextOptionComponent("Destination"),
                ),
                NodesFlow.Node.Option(
                    name="dst", option_component=NodesFlow.InputOptionComponent(dst_value)
                ),
            ]
            masks_human_val = settings.get("masks_human", False)
            masks_machine_val = settings.get("masks_machine", False)
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Add human masks",
                    option_component=NodesFlow.CheckboxOptionComponent(masks_human_val),
                ),
                NodesFlow.Node.Option(
                    name="Set human masks colors",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=human_masks_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            human_masks_widgets_container
                        ),
                        sidebar_width=600,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="human_colors_preview",
                    option_component=NodesFlow.WidgetOptionComponent(human_classes_colors_preview),
                ),
                NodesFlow.Node.Option(
                    name="Add machine masks",
                    option_component=NodesFlow.CheckboxOptionComponent(masks_machine_val),
                ),
                NodesFlow.Node.Option(
                    name="Set machine masks colors",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=machine_masks_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            machine_masks_widgets_container
                        ),
                        sidebar_width=600,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="machine_colors_preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        machine_classes_colors_preview
                    ),
                ),
            ]
            return {
                "src": [],
                "dst": dst_options,
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            get_dst=get_dst,
            meta_changed_cb=meta_changed_cb,
        )

    @classmethod
    def create_outputs(cls):
        return []

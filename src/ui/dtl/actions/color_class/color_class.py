from typing import Optional

from supervisely.app.widgets import NodesFlow, Button, Container, Text
from supervisely import ProjectMeta
from supervisely.imaging.color import hex2rgb, rgb2hex

from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesColorMapping, ClassesMappingPreview
from src.ui.dtl.utils import get_set_settings_button_style, get_set_settings_container, get_layer_docs


class ColorClassAction(AnnotationAction):
    name = "color_class"
    title = "Color Class"
    description = "Use for coloring classes as you wish. Add this class at the end of graph, before data saving."
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/color_class"
    )
    md_description = get_layer_docs()

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes_colors = ClassesColorMapping()
        classes_colors_preview = ClassesMappingPreview()
        classes_colors_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        classes_colors_widgets_container = Container(
            widgets=[classes_colors, classes_colors_save_btn]
        )
        classes_colors_edit_text = Text("Classes Mapping")
        classes_colors_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        classes_colors_edit_conatiner = get_set_settings_container(
            classes_colors_edit_text, classes_colors_edit_btn
        )

        saved_classes_colors_settings = {}

        def _save_classes_colors_setting():
            nonlocal saved_classes_colors_settings
            mapping = classes_colors.get_mapping()
            saved_classes_colors_settings = {
                cls_name: hex2rgb(value["value"]) for cls_name, value in mapping.items()
            }
            obj_classes = classes_colors.get_classes()
            classes_colors_preview.set(
                obj_classes, {k: rgb2hex(v) for k, v in saved_classes_colors_settings.items()}
            )

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {"classes_color_mapping": saved_classes_colors_settings}

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
            classes_colors.loading = True
            classes_colors.set(project_meta.obj_classes)
            _save_classes_colors_setting()
            classes_colors.loading = False

        def _set_settings_from_json(settings: dict):
            colors = settings.get("classes_color_mapping", {})
            classes_colors.loading = True
            classes_colors.set_colors(
                [
                    colors.get(cls, hex2rgb(value["value"]))
                    for cls, value in classes_colors.get_mapping().items()
                ]
            )
            _save_classes_colors_setting()
            classes_colors.loading = False

        classes_colors_save_btn.click(_save_classes_colors_setting)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)

            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Colors",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=classes_colors_edit_conatiner,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_colors_widgets_container
                        ),
                        sidebar_width=600,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="colors_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_colors_preview),
                ),
            ]
            return {
                "src": [],
                "dst": [],
                "settings": settings_options,
            }

        return Layer(
            action=cls,
            id=layer_id,
            create_options=create_options,
            get_settings=get_settings,
            meta_changed_cb=meta_changed_cb,
        )

import copy
import os
from pathlib import Path
from typing import Optional

from supervisely import ProjectMeta, Bitmap, AnyGeometry
from supervisely.app.widgets import NodesFlow, Button, Container, Flexbox

import src.globals as g
from src.ui.dtl import AnnotationAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesMapping, ClassesMappingPreview
from src.ui.dtl.utils import (
    get_classes_mapping_value,
    classes_mapping_settings_changed_meta,
    set_classes_mapping_preview,
    set_classes_mapping_settings_from_json,
)


class Bitmap2LinesAction(AnnotationAction):
    name = "bitmap2lines"
    title = "Bitmap to Lines"
    docs_url = (
        "https://docs.supervisely.com/data-manipulation/index/transformation-layers/bitmap2lines"
    )
    description = "This layer (bitmap2lines) converts thinned (skeletonized) bitmaps to lines. It is extremely useful if you have some raster objects representing lines or edges, maybe forming some tree or net structure, and want to work with vector objects. Each input bitmap should be already thinned (use Skeletonize layer to do it), and for single input mask a number of lines will be produced. Resulting lines may have very many vertices, so consider applying Approx Vector layer to results of this layer. Internally the layer builds a graph of 8-connected pixels, determines minimum spanning tree(s), then greedely extracts diameters from connected components of the tree."

    md_description = ""
    for p in ("readme.md", "README.md"):
        p = Path(os.path.realpath(__file__)).parent.joinpath(p)
        if p.exists():
            with open(p) as f:
                md_description = f.read()
            break

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        classes_mapping_widget = ClassesMapping()
        classes_mapping_preview = ClassesMappingPreview()
        classes_mapping_save_btn = Button("Save", icon="zmdi zmdi-floppy")
        classes_mapping_set_default_btn = Button("Set Default", icon="zmdi zmdi-refresh")
        classes_mapping_widgets_container = Container(
            widgets=[
                classes_mapping_widget,
                Flexbox(
                    widgets=[
                        classes_mapping_save_btn,
                        classes_mapping_set_default_btn,
                    ],
                    gap=355,
                ),
            ]
        )

        saved_classes_mapping_settings = {}
        default_classes_mapping_settings = {}

        def _get_classes_mapping_value():
            return get_classes_mapping_value(
                classes_mapping_widget,
                default_action="skip",
                ignore_action="skip",
                other_allowed=False,
                default_allowed=False,
            )

        def _set_classes_mapping_preview():
            set_classes_mapping_preview(
                classes_mapping_widget,
                classes_mapping_preview,
                saved_classes_mapping_settings,
                default_action="skip",
                ignore_action="skip",
            )

        def _save_classes_mapping_setting():
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = _get_classes_mapping_value()
            set_classes_mapping_preview(
                classes_mapping_widget,
                classes_mapping_preview,
                saved_classes_mapping_settings,
                default_action="skip",
                ignore_action="skip",
            )

        def _set_default_classes_mapping_setting():
            # save setting to var
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = copy.deepcopy(default_classes_mapping_settings)

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            return {
                "classes_mapping": saved_classes_mapping_settings,
                "min_points_cnt": options_json["min_points_cnt"],
            }

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta
            classes_mapping_widget.loading = True
            old_obj_classes = classes_mapping_widget.get_classes()
            new_obj_classes = [
                obj_class
                for obj_class in project_meta.obj_classes
                if obj_class.geometry_type in [Bitmap, AnyGeometry]
            ]

            # set classes to widget
            classes_mapping_widget.set(new_obj_classes)

            # update settings according to new meta
            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = classes_mapping_settings_changed_meta(
                saved_classes_mapping_settings,
                old_obj_classes,
                new_obj_classes,
                default_action="skip",
                ignore_action="skip",
                other_allowed=False,
            )

            # update settings preview
            _set_classes_mapping_preview()

            classes_mapping_widget.loading = False

        def _set_settings_from_json(settings):
            # if settings is empty, set default
            if settings.get("classes_mapping", "default") == "default":
                classes_mapping_widget.set_default()
            else:
                set_classes_mapping_settings_from_json(
                    classes_mapping_widget,
                    settings["classes_mapping"],
                    missing_in_settings_action="ignore",
                    missing_in_meta_action="ignore",
                )

            # save settings
            _save_classes_mapping_setting()
            # update settings preview
            _set_classes_mapping_preview()

        @classes_mapping_save_btn.click
        def classes_mapping_save_btn_cb():
            _save_classes_mapping_setting()
            _set_classes_mapping_preview()
            g.updater("metas")

        @classes_mapping_set_default_btn.click
        def classes_mapping_set_default_btn_cb():
            _set_default_classes_mapping_setting()
            set_classes_mapping_settings_from_json(
                classes_mapping_widget,
                saved_classes_mapping_settings,
                missing_in_settings_action="ignore",
                missing_in_meta_action="ignore",
            )
            _set_classes_mapping_preview()
            g.updater("metas")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            min_points_cnt_val = settings.get("min_points_cnt", 2)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Set Classes Mapping",
                    option_component=NodesFlow.ButtonOptionComponent(
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_mapping_widgets_container
                        ),
                        sidebar_width=630,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="classes_mapping_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_mapping_preview),
                ),
                NodesFlow.Node.Option(
                    name="min_points_cnt",
                    option_component=NodesFlow.IntegerOptionComponent(
                        min=2, default_value=min_points_cnt_val
                    ),
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

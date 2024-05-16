from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import ImgAugAugmentationsAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import (
    get_layer_docs,
    get_text_font_size,
    get_slider_style,
    classes_list_to_mapping,
)

from supervisely import ProjectMeta, Polygon, AnyGeometry
from supervisely.app.widgets import (
    Text,
    NodesFlow,
    Checkbox,
    NotificationBox,
    Slider,
    InputNumber,
    Field,
    Container,
)


class PerspectiveTransformaAction(ImgAugAugmentationsAction):
    name = "perspective_transform"
    title = "iaa.geometric Perspective Transform"
    docs_url = "https://imgaug.readthedocs.io/en/latest/source/overview/geometric.html#perspectivetransform"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    width = 355

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        saved_classes_mapping_settings = "default"

        DEFAULT_SCALE = [0.01, 0.15]
        DEFAULT_CVAL = 0

        scale_input = Slider(
            value=DEFAULT_SCALE, step=0.01, min=0.01, max=0.5, range=True, style=get_slider_style()
        )
        scale_preview_widget = Text(
            f"min:{DEFAULT_SCALE[0]} - max: {DEFAULT_SCALE[1]}",
            status="text",
            font_size=get_text_font_size,
        )
        scale_field = Field(
            title="Scale",
            description="",
            content=Container(widgets=[scale_preview_widget, scale_input]),
        )  # todo desc

        keep_size_checkbox = Checkbox(content="Keep image size")
        keep_box_field = Field(
            title="Keep original image size", description="Ipsum Lorem", content=keep_size_checkbox
        )  # todo desc
        fit_checkbox = Checkbox("Fit to Output")

        cval_input = InputNumber(value=DEFAULT_CVAL, min=0, max=255, step=1, controls=True)
        cval_field = Field(
            title="cval", description="", content=Container(widgets=[cval_input])
        )  # todo desc

        convert_notification = NotificationBox(
            title="Polygon labels will be converted to Bitmap",
            description=(
                "This change ensures that label boundaries are accurately "
                "represented for more precise augmentation results"
            ),
            box_type="info",
        )
        convert_checkbox = Checkbox(content="Convert Polygon labels to Bitmap", checked=True)
        convert_checkbox.disable()

        @scale_input.value_changed
        def scale_slider_value_changed(value):
            scale_preview_widget.text = f"min: {value[0]} - max: {value[1]}"

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_classes_mapping_settings
            classes_mapping = saved_classes_mapping_settings
            keep_size = keep_size_checkbox.is_checked()
            fit = fit_checkbox.is_checked()
            cval = cval_input.get_value()

            scale_min, scale_max = scale_input.get_value()

            if saved_classes_mapping_settings == "default":
                classes_mapping = _get_classes_mapping_value()
            return {
                "scale": {
                    "min": scale_min,
                    "max": scale_max,
                },
                "classes_mapping": classes_mapping,
                "size_box": {"keep": keep_size, "fit": fit},
                "cval": {"value": cval},
            }

        def data_changed_cb(**kwargs):
            project_meta = kwargs.get("project_meta", None)
            if project_meta is None:
                return
            nonlocal _current_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            oc_to_convert = [
                obj_class
                for obj_class in project_meta.obj_classes
                if obj_class.geometry_type in [Polygon, AnyGeometry]
            ]

            nonlocal saved_classes_mapping_settings
            saved_classes_mapping_settings = {oc.name: oc.name for oc in oc_to_convert}

        def _update_preview():
            scale_min, scale_max = scale_input.get_value()
            scale_preview_widget.set(text=f"min: {scale_min} - max: {scale_max}", status="text")

        def _set_settings_from_json(settings: dict):
            scale_input.value = settings.get("scale", 0.01)
            if "size_box" in settings:
                keep_size: dict = settings["size_box"].get("keep", True)
                fit: dict = settings["size_box"].get("fit", False)
            else:
                fit = False
                keep_size = True

            if keep_size:
                keep_size_checkbox.check()
            else:
                keep_size_checkbox.uncheck()

            if fit:
                fit_checkbox.check()
            else:
                fit_checkbox.uncheck()

            _update_preview()

        def _get_classes_mapping_value():
            nonlocal _current_meta
            classes = [obj_class.name for obj_class in _current_meta.obj_classes]
            return classes_list_to_mapping(classes, classes, other="skip")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="scale_text",
                    option_component=NodesFlow.WidgetOptionComponent(scale_field),
                ),
                NodesFlow.Node.Option(
                    name="keep_size_checkbox",
                    option_component=NodesFlow.WidgetOptionComponent(keep_size_checkbox),
                ),
                NodesFlow.Node.Option(
                    name="fit_checkbox",
                    option_component=NodesFlow.WidgetOptionComponent(fit_checkbox),
                ),
                NodesFlow.Node.Option(
                    name="cval_text",
                    option_component=NodesFlow.WidgetOptionComponent(cval_text),
                ),
                NodesFlow.Node.Option(
                    name="cval",
                    option_component=NodesFlow.WidgetOptionComponent(cval_input),
                ),
                NodesFlow.Node.Option(
                    name="notification",
                    option_component=NodesFlow.WidgetOptionComponent(convert_notification),
                ),
                NodesFlow.Node.Option(
                    name="checkbox",
                    option_component=NodesFlow.WidgetOptionComponent(convert_checkbox),
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
            need_preview=True,
            data_changed_cb=data_changed_cb,
        )

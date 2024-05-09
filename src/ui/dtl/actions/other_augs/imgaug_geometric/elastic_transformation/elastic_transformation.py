from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAugmentationsAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size, get_slider_style

from supervisely import ProjectMeta, Polygon, AnyGeometry

from src.ui.dtl.utils import classes_list_to_mapping

from supervisely.app.widgets import Text, NodesFlow, Checkbox, NotificationBox, Slider


class ElasticTransformationAction(OtherAugmentationsAction):
    name = "elastic_transformation"
    title = "Elastic Transformation"
    docs_url = "https://imgaug.readthedocs.io/en/latest/source/overview/imgcorruptlike.html#elastictransform"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    width = 355

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        saved_classes_mapping_settings = "default"

        DEFAULT_ALPHA = [0, 40]
        DEFAULT_SIGMA = [4, 8]
        alpha_text = Text("Alpha", status="text", font_size=get_text_font_size())
        alpha_input = Slider(
            value=DEFAULT_ALPHA, step=1, min=0, max=200, range=True, style=get_slider_style()
        )
        alpha_preview_widget = Text(
            f"min:{DEFAULT_ALPHA[0]} - max: {DEFAULT_ALPHA[1]}",
            status="text",
            font_size=get_text_font_size,
        )

        @alpha_input.value_changed
        def alpha_slider_value_changed(value):
            alpha_preview_widget.text = f"min: {value[0]} - max: {value[1]}"

        sigma_text = Text("Sigma", status="text", font_size=get_text_font_size())
        sigma_input = Slider(
            value=DEFAULT_SIGMA, step=1, min=0, max=50, range=True, style=get_slider_style()
        )
        sigma_preview_widget = Text(
            f"min:{DEFAULT_SIGMA[0]} - max: {DEFAULT_SIGMA[1]}",
            status="text",
            font_size=get_text_font_size,
        )

        @sigma_input.value_changed
        def sigma_slider_value_changed(value):
            sigma_preview_widget.text = f"min: {value[0]} - max: {value[1]}"

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

        def get_settings(options_json: dict) -> dict:
            nonlocal saved_classes_mapping_settings
            classes_mapping = saved_classes_mapping_settings

            alpha_min, alpha_max = alpha_input.get_value()
            sigma_min, sigma_max = sigma_input.get_value()

            if saved_classes_mapping_settings == "default":
                classes_mapping = _get_classes_mapping_value()
            return {
                "alpha": {
                    "min": alpha_min,
                    "max": alpha_max,
                },
                "sigma": {
                    "min": sigma_min,
                    "max": sigma_max,
                },
                "classes_mapping": classes_mapping,
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
            sigma_min, sigma_max = sigma_input.get_value()
            sigma_preview_widget.set(text=f"min: {sigma_min} - max: {sigma_max}", status="text")
            alpha_min, alpha_max = alpha_input.get_value()
            alpha_preview_widget.set(text=f"min: {alpha_min} - max: {alpha_max}", status="text")

        def _set_settings_from_json(settings: dict):
            alpha_input.value = settings.get("alpha", 10)
            sigma_input.value = settings.get("sigma", 1)

            _update_preview()

        def _get_classes_mapping_value():
            nonlocal _current_meta
            classes = [obj_class.name for obj_class in _current_meta.obj_classes]
            return classes_list_to_mapping(classes, classes, other="skip")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="alpha_text",
                    option_component=NodesFlow.WidgetOptionComponent(alpha_text),
                ),
                NodesFlow.Node.Option(
                    name="alpha_preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=alpha_preview_widget,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="alpha",
                    option_component=NodesFlow.WidgetOptionComponent(alpha_input),
                ),
                NodesFlow.Node.Option(
                    name="sigma_text",
                    option_component=NodesFlow.WidgetOptionComponent(sigma_text),
                ),
                NodesFlow.Node.Option(
                    name="sigma_preview",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=sigma_preview_widget,
                    ),
                ),
                NodesFlow.Node.Option(
                    name="sigma",
                    option_component=NodesFlow.WidgetOptionComponent(sigma_input),
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

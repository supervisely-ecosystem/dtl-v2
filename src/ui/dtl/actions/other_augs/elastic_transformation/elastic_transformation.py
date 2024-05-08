from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAugmentationsAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs, get_text_font_size

from supervisely import ProjectMeta, Polygon, AnyGeometry

from src.ui.dtl.utils import classes_list_to_mapping

from supervisely.app.widgets import Text, NodesFlow, InputNumber, Checkbox, NotificationBox


class ElasticTransformationAction(OtherAugmentationsAction):
    name = "elastic_transformation"
    title = "Elastic Transformation"
    docs_url = ""
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    width = 355

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        saved_classes_mapping_settings = "default"
        alpha_text = Text("Alpha", status="text", font_size=get_text_font_size())
        alpha_input = InputNumber(value=10.000, step=0.1, precision=3, controls=True, size="small")

        sigma_text = Text("Sigma", status="text", font_size=get_text_font_size())
        sigma_input = InputNumber(value=1.000, step=0.1, controls=True, size="small")

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
            if saved_classes_mapping_settings == "default":
                classes_mapping = _get_classes_mapping_value()
            return {
                "alpha": alpha_input.get_value(),
                "sigma": sigma_input.get_value(),
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

        def _set_settings_from_json(settings: dict):
            alpha_input.value = settings.get("alpha", 10)
            sigma_input.value = settings.get("sigma", 1)

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
                    name="alpha",
                    option_component=NodesFlow.WidgetOptionComponent(alpha_input),
                ),
                NodesFlow.Node.Option(
                    name="sigma_text",
                    option_component=NodesFlow.WidgetOptionComponent(sigma_text),
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

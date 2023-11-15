import copy
from typing import Optional
from os.path import realpath, dirname

from supervisely.app.widgets import (
    NodesFlow,
    Button,
    Container,
    Flexbox,
    Text,
    Field,
    Select,
    ModelInfo,
    SelectAppSession,
    MatchObjClasses,
    NotificationBox,
)
from supervisely import ProjectMeta
from supervisely.nn.inference import Session, SessionJSON
from supervisely.imaging.color import hex2rgb, rgb2hex

from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList, ClassesListPreview
from src.ui.dtl.utils import (
    classes_list_settings_changed_meta,
    get_classes_list_value,
    set_classes_list_preview,
    set_classes_list_settings_from_json,
    get_set_settings_button_style,
    get_set_settings_container,
    get_layer_docs,
    create_save_btn,
    create_set_default_btn,
    get_text_font_size,
)
import src.globals as g

SESSION_TAGS = [
    "deployed_nn",
    "deployed_nn_cls",
    # "deployed_nn_3d",
    # "sly_video_tracking",
    # "sly_smart_annotation",
    # "deployed_nn_embeddings",
    # "sly_point_cloud_tracking",
    # "deployed_nn_recommendations",
    # "labeling_jobs",
    # "sly_interpolation",
]


class ApplyNNAction(NeuralNetworkAction):
    name = "apply_nn"
    title = "Apply NN"
    docs_url = ""
    description = "Connect to deployed model and select apply options."
    md_description = get_layer_docs(dirname(realpath(__file__)))

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        _current_meta = ProjectMeta()
        _model_meta = ProjectMeta()
        _model_info = {}

        connect_nn_text = Text("Connect to Model", "text", font_size=get_text_font_size())
        connect_nn_model_preview = Text("No model selected", "text", font_size=get_text_font_size())
        connect_nn_edit_btn = Button(
            text="CONNECT",
            icon="zmdi zmdi-router",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        connect_nn_edit_container = get_set_settings_container(connect_nn_text, connect_nn_edit_btn)
        connect_nn_save_btn = create_save_btn()
        connect_nn_model_selector = SelectAppSession(team_id=g.TEAM_ID, tags=SESSION_TAGS)

        connect_nn_model_field = Field(
            title="Select deployed model",
            description="Select deployed model that will be applied for inference",
            content=connect_nn_model_selector,
        )

        connect_nn_model_info = ModelInfo()
        connect_nn_widgets_container = Container(
            widgets=[connect_nn_model_field, connect_nn_model_info, connect_nn_save_btn]
        )

        @connect_nn_model_selector.value_changed
        def set_model_info(session_id):
            if session_id is None:
                return

            connect_nn_model_info.loading = True
            connect_nn_model_info.set_session_id(session_id)
            connect_nn_model_info.loading = False

        @connect_nn_save_btn.click
        def set_nn_model_classes():
            nonlocal _current_meta, _model_meta, _model_info
            match_obj_classes_widget.hide()

            session_id = connect_nn_model_info._session_id
            if session_id is None:
                return

            session = Session(g.api, session_id)
            _model_meta = session.get_model_meta()

            session_json = SessionJSON(g.api, session_id)
            _model_info = session_json.get_session_info()

            model_name = _model_info["app_name"]
            connect_nn_model_preview.set(model_name, "text")

            # use MatchObjClasses
            original_classes, conflict_classes = get_conflict_classes(_current_meta, _model_meta)
            if len(conflict_classes) > 0:
                match_obj_classes_widget.set(original_classes, conflict_classes)
                match_obj_classes_widget.show()
                classes_list_widget_notification.set(
                    title="Classes conflict",
                    description="Project meta and model meta have classes with the same names, but different shapes. Disable conflicting classes in previous nodes or select other model.",
                )
                return

            classes_list_widget_notification.set(
                title="No classes",
                description="Connect node and ensure that source node produces classes of type needed for this node.",
            )
            set_model_classes_to_widget(_model_meta)
            classes_list_widget.select_all()
            # classes_list_save_btn.click()
            _save_classes_list_settings()
            # _set_classes_list_preview()

        def set_model_classes_to_widget(_model_meta):
            classes_list_widget.loading = True
            obj_classes = [cls for cls in _model_meta.obj_classes]

            # set classes to widget
            classes_list_widget.set(obj_classes)

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = classes_list_settings_changed_meta(
                saved_classes_settings, obj_classes, True
            )
            # update settings preview
            _set_classes_list_preview()
            classes_list_widget.loading = False

        def get_conflict_classes(current_meta, model_meta):
            original_classess = []
            conflict_classes = []
            for curr_obj_class in current_meta.obj_classes:
                model_obj_class = model_meta.get_obj_class(curr_obj_class.name)
                if model_obj_class is not None:
                    if curr_obj_class.geometry_type != model_obj_class.geometry_type:
                        original_classess.append(curr_obj_class)
                        conflict_classes.append(model_obj_class)
            return original_classess, conflict_classes

        match_obj_classes_widget = MatchObjClasses()
        match_obj_classes_widget.hide()

        classes_list_widget_notification = NotificationBox(
            title="No classes",
            description="Connect node and ensure that source node produces classes of type needed for this node.",
        )
        classes_list_widget = ClassesList(
            multiple=True, empty_notification=classes_list_widget_notification
        )
        classes_list_preview = ClassesListPreview(empty_text="No classes selected")
        classes_list_save_btn = create_save_btn()
        classes_list_set_default_btn = create_set_default_btn()

        classes_list_widget_field = Field(
            content=classes_list_widget,
            title="Model Classes",
            description="Select classes from model",
        )
        classes_list_widgets_container = Container(
            widgets=[
                classes_list_widget_field,
                match_obj_classes_widget,
                Flexbox(
                    widgets=[
                        classes_list_save_btn,
                        classes_list_set_default_btn,
                    ],
                    gap=110,
                ),
            ]
        )
        classes_list_edit_text = Text(
            "Model Classes", status="text", font_size=get_text_font_size()
        )
        classes_list_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        classes_list_edit_container = get_set_settings_container(
            classes_list_edit_text, classes_list_edit_btn
        )

        saved_classes_settings = "default"
        default_classes_settings = "default"

        def _get_classes_list_value():
            return get_classes_list_value(classes_list_widget, multiple=True)

        def _set_classes_list_preview():
            set_classes_list_preview(
                classes_list_widget, classes_list_preview, saved_classes_settings
            )

        def _save_classes_list_settings():
            nonlocal saved_classes_settings
            saved_classes_settings = _get_classes_list_value()

        def _set_default_classes_list_setting():
            # save setting to var
            nonlocal saved_classes_settings
            saved_classes_settings = copy.deepcopy(default_classes_settings)

        apply_nn_selector_methods = [
            Select.Item("image", "Full Image"),
            Select.Item("roi", "ROI defined by object BBox"),
        ]
        apply_nn_method_text = Text("Apply method", font_size=get_text_font_size())
        apply_nn_methods_selector = Select(items=apply_nn_selector_methods, size="small")

        apply_nn_methods_selector.disable()  # disable ROI

        anonymize_type_container = Container(
            widgets=[
                apply_nn_method_text,
                Flexbox(
                    widgets=[apply_nn_methods_selector],
                ),
            ],
            style="margin-top: 15px;",
            gap=4,
        )

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta
            if project_meta == _current_meta:
                return

            _current_meta = project_meta

            classes_list_widget.loading = True
            obj_classes = [cls for cls in project_meta.obj_classes]

            # set classes to widget
            # classes_list_widget.set(obj_classes)

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = classes_list_settings_changed_meta(
                saved_classes_settings, obj_classes, True
            )

            # comment to hide classes preview on node link
            # update settings preview
            # _set_classes_list_preview()

            classes_list_widget.loading = False

        def unpack_selected_model_classes(saved_classes_settings):
            nonlocal _model_meta
            selected_model_classes = []
            for obj_class in _model_meta.obj_classes:
                if obj_class.name in saved_classes_settings:
                    selected_model_classes.append(
                        {
                            "name": obj_class.name,
                            "shape": obj_class.geometry_type.__name__.lower(),
                            "color": obj_class.color,
                        }
                    )

            return selected_model_classes

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            apply_method = apply_nn_methods_selector.get_value()
            selected_model_classes = unpack_selected_model_classes(saved_classes_settings)
            settings = {
                "session_id": connect_nn_model_info._session_id,
                "model_info": _model_info,
                "classes": selected_model_classes,
                "apply_method": apply_method,
            }
            return settings

        def _set_settings_from_json(settings: dict):
            apply_method = settings.get("type", "image")
            apply_nn_methods_selector.set_value(apply_method)

            classes_list_widget.loading = True
            classes_list_settings = settings.get("classes", [])
            set_classes_list_settings_from_json(
                classes_list_widget=classes_list_widget, settings=classes_list_settings
            )
            # save settings
            _save_classes_list_settings()
            # update settings preview
            _set_classes_list_preview()
            classes_list_widget.loading = False

        @classes_list_save_btn.click
        def classes_list_save_btn_cb():
            _save_classes_list_settings()
            _set_classes_list_preview()
            g.updater("metas")

        @classes_list_set_default_btn.click
        def classes_list_set_default_btn_cb():
            _set_default_classes_list_setting()
            set_classes_list_settings_from_json(
                classes_list_widget=classes_list_widget, settings=saved_classes_settings
            )
            _set_classes_list_preview()
            g.updater("metas")

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Connect to Model",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=connect_nn_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            connect_nn_widgets_container
                        ),
                        sidebar_width=380,
                    ),
                ),
                NodesFlow.Node.Option(
                    "model_preview",
                    option_component=NodesFlow.WidgetOptionComponent(connect_nn_model_preview),
                ),
                NodesFlow.Node.Option(
                    name="Select Classes",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=classes_list_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            classes_list_widgets_container
                        ),
                        sidebar_width=600,
                    ),
                ),
                NodesFlow.Node.Option(
                    "classes_preview",
                    option_component=NodesFlow.WidgetOptionComponent(classes_list_preview),
                ),
                NodesFlow.Node.Option(
                    "anonymize_type",
                    option_component=NodesFlow.WidgetOptionComponent(anonymize_type_container),
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

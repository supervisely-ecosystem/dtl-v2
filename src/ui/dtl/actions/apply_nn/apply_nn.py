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
    MatchTagMetas,
    NotificationBox,
)
from supervisely import ProjectMeta
from supervisely.nn.inference import Session, SessionJSON
from supervisely.imaging.color import hex2rgb, rgb2hex
from supervisely import TagMeta, ObjClass
from src.ui.dtl import NeuralNetworkAction
from src.ui.dtl.Layer import Layer
from src.ui.widgets import ClassesList, ClassesListPreview, TagsList, TagMetasPreview
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
    set_tags_list_settings_from_json,
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

        ### UPDATE BUTTON
        update_preview_btn = Button(
            text="Update",
            icon="zmdi zmdi-refresh",
            button_type="text",
            button_size="small",
            style=get_set_settings_button_style(),
        )
        update_preview_btn.disable()
        ### -----------------------------

        ### CONNECT TO MODEL
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
        connect_nn_model_info_empty_text = Text("Select model to display info", "text")
        connect_nn_model_info_container = Container(
            [connect_nn_model_info, connect_nn_model_info_empty_text]
        )
        connect_nn_model_info_field = Field(
            title="Model Info",
            description="Technical details and configurations for deployed model",
            content=connect_nn_model_info_container,
        )

        connect_nn_widgets_container = Container(
            widgets=[connect_nn_model_field, connect_nn_model_info_field, connect_nn_save_btn]
        )

        @connect_nn_model_selector.value_changed
        def set_model_info(session_id):
            if session_id is None:
                return

            connect_nn_model_info_empty_text.loading = True
            try:
                connect_nn_model_info.loading = True
                connect_nn_model_info.set_session_id(session_id)
            except:
                connect_nn_model_info_empty_text.set(
                    "Couldn't connect to model. Check deployed model logs", status="error"
                )
                connect_nn_model_info.loading = False
                connect_nn_model_info_empty_text.loading = False
                return

            connect_nn_model_info.loading = False
            connect_nn_model_info_empty_text.loading = False
            connect_nn_model_info_empty_text.hide()

        @connect_nn_save_btn.click
        def set_nn_model_classes():
            nonlocal _current_meta, _model_meta, _model_info
            update_preview_btn.disable()

            match_obj_classes_widget.hide()
            match_tag_metas_widget.hide()

            session_id = connect_nn_model_info._session_id
            if session_id is None:
                return

            try:
                session = Session(g.api, session_id)
                _model_meta = session.get_model_meta()

                session_json = SessionJSON(g.api, session_id)
                _model_info = session_json.get_session_info()
            except:
                raise ConnectionError("Couldn't connect to model. Check deployed model logs")

            model_name = _model_info["app_name"]
            connect_nn_model_preview.set(model_name, "text")

            has_classes_conflict = check_conflict_classes(_current_meta, _model_meta)
            has_tags_conflict = check_conflict_tags(_current_meta, _model_meta)

            if not has_classes_conflict and not has_tags_conflict:
                update_preview_btn.enable()
                g.updater("metas")

        def set_model_classes_to_widget(_model_meta: ProjectMeta):
            classes_list_widget.loading = True
            obj_classes = [obj_class for obj_class in _model_meta.obj_classes]

            # set classes to widget
            classes_list_widget.set(obj_classes)
            classes_list_widget.select_all()

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = [obj_class.name for obj_class in _model_meta.obj_classes]
            # update settings preview
            _set_classes_list_preview()
            classes_list_widget.loading = False

            # remove
            # classes_list_widget.select_all()
            # classes_list_preview.set(obj_classes)

        def set_model_tags_to_widget(_model_meta: ProjectMeta):
            tags_list_widget.loading = True
            tag_metas = [tag_meta for tag_meta in _model_meta.tag_metas]

            # set classes to widget
            tags_list_widget.set(tag_metas)
            tags_list_widget.select_all()

            # update settings according to new meta
            nonlocal saved_tags_settings
            saved_tags_settings = tag_metas
            # update settings preview
            _set_tags_list_preview()
            tags_list_widget.loading = False

            # remove
            # tags_list_preview.set(tag_metas)
            # tags_list_widget.select_all()

        def check_conflict_classes(current_meta: ProjectMeta, model_meta: ProjectMeta) -> bool:
            match_obj_classes_widget.hide()
            classes_list_widget.hide()

            has_classes_conflict = False
            original_classes = []
            conflict_classes = []
            for curr_obj_class in current_meta.obj_classes:
                model_obj_class = model_meta.get_obj_class(curr_obj_class.name)
                if model_obj_class is not None:
                    if curr_obj_class.geometry_type != model_obj_class.geometry_type:
                        original_classes.append(curr_obj_class)
                        conflict_classes.append(model_obj_class)

            if len(conflict_classes) > 0:
                has_classes_conflict = True
                match_obj_classes_widget.set(original_classes, conflict_classes)
                classes_list_widget_notification.set(
                    title="Classes conflict",
                    description="Project meta and model meta have classes with the same names, but different shapes. Disable conflicting classes in previous nodes or select other model.",
                )
                match_obj_classes_widget.show()
            else:
                classes_list_widget_notification.set(
                    title="No classes",
                    description="Connect to deployed model to display classes.",
                )
                if len(_model_meta.obj_classes) == 0:
                    classes_list_widget_notification.show()

            if not has_classes_conflict:
                classes_list_widget.show()

            if len(_model_meta.obj_classes) > 0 and not has_classes_conflict:
                set_model_classes_to_widget(_model_meta)
            else:
                set_model_classes_to_widget(ProjectMeta())

            return has_classes_conflict

        def check_conflict_tags(current_meta: ProjectMeta, model_meta: ProjectMeta) -> bool:
            tags_list_widget_notification.hide()
            tags_list_widget.hide()

            has_tags_conflict = False
            original_tags = []
            conflict_tags = []
            for curr_tag_meta in current_meta.tag_metas:
                model_tag_meta = model_meta.get_tag_meta(curr_tag_meta.name)
                if model_tag_meta is not None:
                    original_tags.append(curr_tag_meta)
                    conflict_tags.append(model_tag_meta)

            if len(conflict_tags) > 0:
                match_tag_metas_widget.set(original_tags, conflict_tags)
                conflict_stat = match_tag_metas_widget.get_stat()
                if (
                    conflict_stat["different_value_type"] > 0
                    or conflict_stat["different_one_of_options"] > 0
                    or conflict_stat["different_value_type_suffix"] > 0
                    or conflict_stat["different_one_of_options_suffix"] > 0
                ):
                    has_tags_conflict = True
                    tags_list_widget_notification.set(
                        title="Tags conflict",
                        description="Project meta and model meta have tag metas with the same names, but different values. Disable conflicting tags in previous nodes or select other model.",
                    )

            if len(_model_meta.tag_metas) == 0:
                tags_list_widget_notification.set(
                    title="No tags",
                    description="Connect to deployed model to display tags.",
                )

            if not has_tags_conflict:
                tags_list_widget_notification.show()
                tags_list_widget.show()
            else:
                match_tag_metas_widget.show()
                tags_list_widget.hide()

            if len(_model_meta.tag_metas) > 0 and not has_tags_conflict:
                set_model_tags_to_widget(_model_meta)
            else:
                set_model_tags_to_widget(ProjectMeta())
            return has_tags_conflict

        ### -----------------------------

        ### CLASSES
        match_obj_classes_widget = MatchObjClasses()
        match_obj_classes_widget.hide()

        classes_list_widget_notification = NotificationBox(
            title="No classes",
            description="Connect to deployed model to display classes.",
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
        ### -----------------------------

        ### TAGS
        match_tag_metas_widget = MatchTagMetas()
        match_tag_metas_widget.hide()

        tags_list_widget_notification = NotificationBox(
            title="No tags",
            description="Connect to deployed model to display tags.",
        )
        tags_list_widget = TagsList(multiple=True, empty_notification=tags_list_widget_notification)
        tags_list_preview = TagMetasPreview(empty_text="No tags selected")
        tags_list_save_btn = create_save_btn()
        tags_list_set_default_btn = create_set_default_btn()

        tags_list_widget_field = Field(
            content=tags_list_widget,
            title="Model Tags",
            description="Select tags from model",
        )
        tags_list_widgets_container = Container(
            widgets=[
                tags_list_widget_field,
                match_tag_metas_widget,
                Flexbox(
                    widgets=[
                        tags_list_save_btn,
                        tags_list_set_default_btn,
                    ],
                    gap=110,
                ),
            ]
        )

        tags_list_edit_text = Text("Model Tags", status="text", font_size=get_text_font_size())
        tags_list_edit_btn = Button(
            text="EDIT",
            icon="zmdi zmdi-edit",
            button_type="text",
            button_size="small",
            emit_on_click="openSidebar",
            style=get_set_settings_button_style(),
        )
        tags_list_edit_container = get_set_settings_container(
            tags_list_edit_text, tags_list_edit_btn
        )
        ### -----------------------------

        ### APPLY METHOD
        apply_nn_selector_methods = [
            Select.Item("image", "Full Image"),
            Select.Item("roi", "ROI defined by object BBox"),
        ]
        apply_nn_method_text = Text("Apply method", font_size=get_text_font_size())
        apply_nn_methods_selector = Select(items=apply_nn_selector_methods, size="small")

        apply_nn_methods_selector.disable()  # disable ROI

        apply_nn_method_container = Container(
            widgets=[
                apply_nn_method_text,
                Flexbox(
                    widgets=[apply_nn_methods_selector],
                ),
            ],
            style="margin-top: 15px;",
            gap=4,
        )
        ### -----------------------------

        saved_classes_settings = "default"
        default_classes_settings = "default"

        saved_tags_settings = "default"
        default_tags_settings = "default"

        def _get_classes_list_value():
            return get_classes_list_value(classes_list_widget, multiple=True)

        def _get_tags_list_value():
            return [tag_meta for tag_meta in tags_list_widget.get_selected_tags()]

        def _set_classes_list_preview():
            set_classes_list_preview(
                classes_list_widget,
                classes_list_preview,
                [
                    obj_class.name if type(obj_class) == ObjClass else obj_class
                    for obj_class in saved_classes_settings
                ],
            )

        def _set_tags_list_preview():
            tags_list_preview.set([tag_meta for tag_meta in tags_list_widget.get_selected_tags()])

        def _save_classes_list_settings():
            nonlocal saved_classes_settings
            saved_classes_settings = _get_classes_list_value()

        def _save_tags_list_settings():
            nonlocal saved_tags_settings
            saved_tags_settings = _get_tags_list_value()

        def _set_default_classes_list_setting():
            # save setting to var
            nonlocal saved_classes_settings
            saved_classes_settings = copy.deepcopy(default_classes_settings)

        def _set_default_tags_list_setting():
            # save setting to var
            nonlocal saved_tags_settings
            saved_tags_settings = copy.deepcopy(default_tags_settings)

        def meta_changed_cb(project_meta: ProjectMeta):
            nonlocal _current_meta, _model_meta
            if project_meta == _current_meta:
                return
            _current_meta = project_meta

            if connect_nn_model_info.session_id is None:
                return

            classes_list_widget.loading = True
            tags_list_widget.loading = True

            # obj_classes = [obj_class for obj_class in project_meta.obj_classes]
            tag_metas = [tag_meta for tag_meta in project_meta.tag_metas]

            # update settings according to new meta
            nonlocal saved_classes_settings
            saved_classes_settings = [obj_class.name for obj_class in project_meta.obj_classes]
            has_classes_conflicts = check_conflict_classes(_current_meta, _model_meta)

            nonlocal saved_tags_settings
            saved_tags_settings = tag_metas
            has_tags_conflicts = check_conflict_tags(_current_meta, _model_meta)

            classes_list_widget.loading = False
            tags_list_widget.loading = False

            if has_classes_conflicts or has_tags_conflicts:
                update_preview_btn.disable()
            else:
                update_preview_btn.enable()

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

        def unpack_selected_model_tags(saved_tags_settings):
            nonlocal _model_meta
            selected_model_tags = []
            for tag_meta in _model_meta.tag_metas:
                if tag_meta in saved_tags_settings:
                    selected_model_tags.append(
                        {
                            "name": tag_meta.name,
                            "value_type": tag_meta.value_type,
                            "color": tag_meta.color,
                        }
                    )

            return selected_model_tags

        def get_settings(options_json: dict) -> dict:
            """This function is used to get settings from options json we get from NodesFlow widget"""
            apply_method = apply_nn_methods_selector.get_value()
            selected_model_classes = unpack_selected_model_classes(saved_classes_settings)
            selected_model_tags = unpack_selected_model_tags(saved_tags_settings)
            settings = {
                "session_id": connect_nn_model_info._session_id,
                "model_info": _model_info,
                "classes": selected_model_classes,
                "tags": selected_model_tags,
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

        @tags_list_save_btn.click
        def tags_list_save_btn_cb():
            _save_tags_list_settings()
            _set_tags_list_preview()
            g.updater("metas")

        @tags_list_set_default_btn.click
        def tags_list_set_default_btn_cb():
            _set_default_tags_list_setting()
            set_tags_list_settings_from_json(
                tags_list_widget=classes_list_widget, settings=saved_tags_settings
            )
            _set_tags_list_preview()
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
                    name="Select Tags",
                    option_component=NodesFlow.WidgetOptionComponent(
                        widget=tags_list_edit_container,
                        sidebar_component=NodesFlow.WidgetOptionComponent(
                            tags_list_widgets_container
                        ),
                        sidebar_width=600,
                    ),
                ),
                NodesFlow.Node.Option(
                    "tags_preview",
                    option_component=NodesFlow.WidgetOptionComponent(tags_list_preview),
                ),
                NodesFlow.Node.Option(
                    "anonymize_type",
                    option_component=NodesFlow.WidgetOptionComponent(apply_nn_method_container),
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
            custom_update_btn=update_preview_btn,
        )

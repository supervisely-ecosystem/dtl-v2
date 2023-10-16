from typing import List, Literal, Union
from os.path import join, exists

from supervisely import ObjClass, ObjClassCollection
from supervisely.app.widgets import NodesFlow, Container, Text, Button, Empty, ClassesTable

from src.ui.widgets import ClassesMapping, ClassesMappingPreview, ClassesList, ClassesListPreview
from src.exceptions import BadSettingsError


# Classes Mapping utils


def _unpack_classes_mapping_settings(
    mapping: dict, all_obj_classes_names, missing_value: Literal["default", "ignore"] = "ignore"
):
    unpacked = {}
    if mapping == "default":
        for obj_class_name in all_obj_classes_names:
            unpacked[obj_class_name] = obj_class_name
        return unpacked
    missing_value = f"__{missing_value}__"
    other = mapping.get("__other__", None)
    for obj_class_name in all_obj_classes_names:
        old_value = mapping.get(obj_class_name, other)
        if old_value is None:
            old_value = missing_value
        unpacked[obj_class_name] = old_value
    return unpacked


def _pack_classes_mapping_settings(
    mapping: dict,
    default_action: Literal["skip", "keep", "copy"] = "skip",
    ignore_action: Literal["skip", "keep", "empty"] = "skip",
    other_allowed: bool = False,
):
    new_mapping = {}
    for name, value in mapping.items():
        if value in ["__default__", name]:
            if default_action == "skip":
                continue
            elif default_action == "keep":
                new_mapping[name] = "__default__"
            elif default_action == "copy":
                new_mapping[name] = name
        elif value in ["__ignore__", ""]:
            if ignore_action == "skip":
                continue
            elif ignore_action == "keep":
                new_mapping[name] = "__ignore__"
            elif ignore_action == "empty":
                new_mapping[name] = ""
        else:
            new_mapping[name] = value
    if other_allowed:
        default = [name for name, value in new_mapping.items() if value == "__default__"]
        ignore = [name for name, value in new_mapping.items() if value == "__ignore__"]
        if len(ignore) > 0:
            for name in ignore:
                del new_mapping[name]
            new_mapping["__other__"] = "__ignore__"
        elif len(default) > 0:
            for name in default:
                del new_mapping[name]
            new_mapping["__other__"] = "__default__"
    return new_mapping


def get_classes_mapping_value(
    classes_mapping_widget: ClassesMapping,
    default_action: Literal["skip", "keep", "copy"] = "skip",
    ignore_action: Literal["skip", "keep", "empty"] = "skip",
    other_allowed: bool = False,
    default_allowed: bool = False,
):
    mapping = classes_mapping_widget.get_mapping()
    if default_allowed:
        default = [cls_name for cls_name, cls_values in mapping.items() if cls_values["default"]]
        classes = classes_mapping_widget.get_classes()
        if len(default) == len(classes):
            return "default"

    result_mapping = _pack_classes_mapping_settings(
        {k: v["value"] for k, v in mapping.items()},
        default_action=default_action,
        ignore_action=ignore_action,
        other_allowed=other_allowed,
    )

    return result_mapping


def classes_mapping_settings_changed_meta(
    settings: dict,
    old_obj_classes: Union[List[ObjClass], ObjClassCollection],
    new_obj_classes: Union[List[ObjClass], ObjClassCollection],
    default_action: Literal["skip", "keep", "copy"] = "skip",
    ignore_action: Literal["skip", "keep", "empty"] = "skip",
    new_value: Literal["default", "ignore"] = "ignore",
    other_allowed: bool = False,
):
    if settings == "default":
        return "default"
    new_settings = {}

    old_obj_classes_names = {obj_class.name for obj_class in old_obj_classes}
    new_obj_classes_names = {obj_class.name for obj_class in new_obj_classes}

    # unpack old settings
    new_settings = _unpack_classes_mapping_settings(settings, old_obj_classes_names, new_value)

    # remove obj classes that are not in new obj classes
    for obj_class_name in old_obj_classes_names:
        if obj_class_name not in new_obj_classes_names:
            del new_settings[obj_class_name]

    # add new object classes
    for obj_class_name in new_obj_classes_names:
        if obj_class_name not in old_obj_classes_names:
            new_settings[obj_class_name] = f"__{new_value}__"

    # pack new settings
    new_settings = _pack_classes_mapping_settings(
        new_settings,
        default_action=default_action,
        ignore_action=ignore_action,
        other_allowed=other_allowed,
    )
    return new_settings


def set_classes_mapping_preview(
    classes_mapping_widget: ClassesMapping,
    classes_mapping_preview_widget: ClassesMappingPreview,
    classes_mapping_settings: dict,
    default_action: Literal["skip", "keep", "copy"] = "skip",
    ignore_action: Literal["skip", "keep", "empty"] = "skip",
    missing_value: Literal["default", "ignore"] = "ignore",
):
    obj_classes = classes_mapping_widget.get_classes()
    obj_classes_names = [obj_class.name for obj_class in obj_classes]
    unpacked = _unpack_classes_mapping_settings(
        classes_mapping_settings, obj_classes_names, missing_value=missing_value
    )
    packed = _pack_classes_mapping_settings(
        unpacked, default_action=default_action, ignore_action=ignore_action, other_allowed=False
    )
    classes_mapping_preview_widget.set(
        [obj_class for obj_class in obj_classes if obj_class.name in packed], packed
    )


def set_classes_mapping_settings_from_json(
    classes_mapping_widget: ClassesMapping,
    settings: dict,
    missing_in_settings_action: Literal["raise", "ignore"] = "raise",
    missing_in_meta_action: Literal["raise", "ignore"] = "raise",
):
    if settings == "default":
        classes_mapping_widget.set_default()
        return
    classes_mapping = {}
    other_default = settings.get("__other__", None) == "__default__"
    other_ignore = settings.get("__other__", None) == "__ignore__"
    obj_classes = classes_mapping_widget.get_classes()

    # check that all the classes from settings are present in meta
    if missing_in_meta_action == "raise":
        if isinstance(obj_classes, ObjClassCollection):
            in_func = lambda cls_name: obj_classes.has_key(cls_name)
        else:
            in_func = lambda cls_name: cls_name in [obj_class.name for obj_class in obj_classes]
        for cls_name in settings.keys():
            if cls_name != "__other__" and not in_func(cls_name):
                raise BadSettingsError("Class not found in meta", extra={"class": cls_name})

    # set classes mapping to widget
    for obj_class in obj_classes:
        if obj_class.name in settings:
            value = settings[obj_class.name]
            if value == "__default__":
                value = obj_class.name
            if value == "__ignore__":
                value = ""
            classes_mapping[obj_class.name] = value
        elif other_default:
            classes_mapping[obj_class.name] = obj_class.name
        elif other_ignore:
            classes_mapping[obj_class.name] = ""
        elif missing_in_settings_action == "raise":
            raise BadSettingsError(
                "Class not found in settings",
                extra={"class": obj_class.name},
            )
        else:
            classes_mapping[obj_class.name] = ""
    classes_mapping_widget.set_mapping(classes_mapping)


# Classes List utils


def get_classes_list_value(
    classes_list_widget: Union[ClassesList, ClassesTable], multiple: bool = True
):
    selected = classes_list_widget.get_selected_classes()
    if multiple:
        if isinstance(classes_list_widget, ClassesList):
            return [obj_class.name for obj_class in selected]
        else:
            return [obj_class for obj_class in selected]
    else:
        if len(selected) == 0:
            return ""
        return selected[0].name  # add if for ClassesTable w/o .name


def classes_list_settings_changed_meta(
    settings: Union[list, str],
    new_obj_classes: Union[List[ObjClass], ObjClassCollection],
):
    names = {obj_class.name for obj_class in new_obj_classes}
    if isinstance(settings, str):
        return settings if settings in names else ""
    return [class_name for class_name in settings if class_name in names]


def set_classes_list_preview(
    classes_list_widget: Union[ClassesList, ClassesMapping, ClassesTable],
    classes_list_preview_widget: ClassesListPreview,
    classes_list_settings: Union[list, str],
):
    if isinstance(classes_list_settings, str):
        if classes_list_settings == "default":
            if isinstance(classes_list_widget, ClassesMapping):
                classes_list_preview_widget.set(classes_list_widget.get_classes())
            elif isinstance(classes_list_widget, ClassesList):
                classes_list_preview_widget.set(classes_list_widget.get_all_classes())
            else:
                classes_list_widget.select_all()
                meta = classes_list_widget.project_meta
                classes_list_preview_widget.set([obj_class for obj_class in meta.obj_classes])
            return
        names = [classes_list_settings]
    elif isinstance(classes_list_settings, dict):
        names = [name for name in classes_list_settings.keys() if name != "__other__"]
    else:
        names = classes_list_settings

    if not isinstance(classes_list_widget, ClassesTable):
        obj_classes = classes_list_widget.get_all_classes()
        classes_list_preview_widget.set(
            [obj_class for obj_class in obj_classes if obj_class.name in names]
        )
    else:
        obj_classes = classes_list_widget.get_selected_classes()
        meta = classes_list_widget._project_meta
        res_obj_classes = []
        if meta is not None:
            for cls in meta.obj_classes:
                if cls.name in obj_classes:
                    res_obj_classes.append(cls)
        classes_list_preview_widget.set(
            [obj_class for obj_class in res_obj_classes if obj_class.name in names]
        )


def set_classes_list_settings_from_json(
    classes_list_widget: Union[ClassesList, ClassesTable], settings: Union[list, dict, str]
):
    if isinstance(settings, str):
        if settings == "default":
            classes_list_widget.select_all()
            return
        settings = [settings]
    elif isinstance(settings, dict):
        settings = [name for name in settings.keys() if name != "__other__"]

    if isinstance(classes_list_widget, ClassesList):
        classes_list_widget.select(settings)
    elif isinstance(classes_list_widget, ClassesTable):
        classes_list_widget.select_classes(settings)
        return


# Options utils


def get_separator(idx: int = 0):
    return NodesFlow.Node.Option(
        name=f"separator {idx}",
        option_component=NodesFlow.HtmlOptionComponent('<hr style="border-top: 1px solid #ccc;">'),
    )


empty = Empty()


def get_set_settings_container(text: Text, button: Button):
    return Container(
        widgets=[text, empty, button],
        direction="horizontal",
        style="place-items: center",
        gap=0,
        fractions=[6, 1, 3],
    )


def get_set_settings_button_style():
    return "flex: auto; border: 1px solid #bfcbd9; color: black; background-color: white"


# Sidebar action options utils


def create_save_btn() -> Button:
    return Button("Save", icon="zmdi zmdi-floppy", call_on_click="closeSidebar();")


def create_set_default_btn() -> Button:
    return Button("Set Default", button_type="info", plain=True, icon="zmdi zmdi-refresh")


# Layer docs utils


def get_layer_docs(layer_dir: str) -> str:
    md_description = ""
    for p in ("readme.md", "README.md"):
        p = join(layer_dir, p)
        if exists(p):
            with open(p) as f:
                md_description = f.read()
            break
    return md_description


# Widgets utils


def get_slider_style():
    return "padding: 0 7px"


def get_text_font_size():
    return 13

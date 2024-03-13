from typing import Optional
import traceback

from supervisely import logger
from supervisely import ProjectMeta


class CustomException(Exception):
    def __init__(
        self, message: str, error: Optional[Exception] = None, extra: Optional[dict] = None
    ):
        super().__init__(message)
        self.message = message + "." if not message.endswith(".") else ""
        self.error = error
        self.extra = extra

    def __str__(self):
        from src.ui.dtl import actions_dict
        import src.globals as g

        msg = self.message
        extra_text = ""
        if "layer_id" in self.extra:
            layer_id = self.extra["layer_id"]
            try:
                layer_title = g.layers[layer_id].action.title
            except:
                layer_title = layer_id
            extra_text = f" Layer: {layer_title}"
        elif "layer_name" in self.extra:
            try:
                layer_title = actions_dict[self.extra["layer_name"]].title
            except:
                layer_title = self.extra["layer_name"]
            extra_text = f" Layer: {layer_title}"
        elif "layer" in self.extra:
            try:
                layer_title = actions_dict[self.extra["layer"]].title
            except:
                layer_title = self.extra["layer"]
            extra_text = f" Layer: {layer_title}"
        elif "layer_config" in self.extra:
            try:
                action = self.extra["layer_config"]["action"]
                try:
                    layer_title = actions_dict[action].title
                except:
                    layer_title = action
                extra_text = f" Layer: {layer_title}"
            except:
                pass

        return msg + extra_text

    def log(self):
        exc_info = (
            traceback.format_tb(self.error.__traceback__)
            if self.error
            else traceback.format_tb(self.__traceback__)
        )
        logger.error(self.message, exc_info=exc_info, extra=self.extra)


class ActionNotFoundError(CustomException):
    def __init__(self, action_name: str, extra: Optional[dict] = {}):
        self.action_name = action_name
        extra["action_name"] = action_name
        super().__init__("Action not found", extra=extra)


class CreateLayerError(CustomException):
    def __init__(self, action_name: str, error: Exception, extra: Optional[dict] = {}):
        self.action_name = action_name
        extra["action_name"] = action_name
        super().__init__(f"Error creating Layer", error=error, extra=extra)


class LayerNotFoundError(CustomException):
    def __init__(self, layer_id: str, extra: Optional[dict] = {}):
        self.layer_id = layer_id
        extra["layer_id"] = layer_id
        super().__init__("Layer not found", extra=extra)


class CreateNodeError(CustomException):
    def __init__(self, layer_name, error: Exception, extra: Optional[dict] = {}):
        self.layer_name = layer_name
        extra["layer_name"] = layer_name
        super().__init__(f"Error creating Node", error=error, extra=extra)


class UnexpectedError(CustomException):
    def __init__(
        self, message: str = "Unexpected error", error: Exception = None, extra: Optional[dict] = {}
    ):
        super().__init__(message, error=error, extra=extra)


class UpdateMetaError(CustomException):
    def __init__(
        self,
        layer_name: str,
        project_meta: ProjectMeta,
        error: Exception,
        extra: Optional[dict] = {},
    ):
        self.layer_name = layer_name
        self.project_meta = project_meta
        extra["layer_name"] = layer_name
        extra["project_meta"] = project_meta.to_json()
        super().__init__(
            f"Error updating project meta",
            error=error,
            extra=extra,
        )


class BadSettingsError(CustomException):
    def __init__(
        self,
        message,
        error: Exception = None,
        extra: Optional[dict] = {},
    ):
        message = "Bad settings. " + message
        super().__init__(message, error, extra=extra)


class GraphError(CustomException):
    def __init__(self, message, error: Exception = None, extra: Optional[dict] = {}):
        message = "Graph Error. " + message
        super().__init__(message, error=error, extra=extra)


class ValidationError(CustomException):
    def __init__(self, message, error: Exception = None, extra: Optional[dict] = {}):
        message = "Validation Error. " + message
        super().__init__(message, error=error, extra=extra)


class CreateMetaError(CustomException):
    def __init__(self, message, error: Exception = None, extra: Optional[dict] = {}):
        message = "Create Meta Error. " + message
        super().__init__(message, error=error, extra=extra)


class WrongGeometryError(CustomException):
    def __init__(self, message, expected_geometry, got_geometry, extra: Optional[dict] = {}):
        message = f"Wrong geometry. {message+'. ' if message else ''}Expected: {expected_geometry}. Got: {got_geometry}"
        super().__init__(message, extra=extra)


def handle_exception(func):
    """Decorator to log exception and silence it"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as e:
            e.log()
        except Exception as e:
            logger.error("Unexpected error", exc_info=traceback.format_exc())

    return inner

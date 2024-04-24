from typing import Optional
from os.path import realpath, dirname

from src.ui.dtl import OtherAction
from src.ui.dtl.Layer import Layer
from src.ui.dtl.utils import get_layer_docs
from supervisely.app.widgets import NodesFlow, NotificationBox, Checkbox


class MoveAction(OtherAction):
    name = "move"
    title = "Move"
    docs_url = ""
    description = (
        "Move items from the source to the destination. "
        "Items in the source will be removed after the move operation is successfully completed"
    )
    md_description = get_layer_docs(dirname(realpath(__file__)))
    width = 380

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        move_notification = NotificationBox(
            title="Move items from the source to the destination",
            description=(
                "Items in the source project will be removed after the move operation is successfully completed"
            ),
            box_type="info",
        )
        move_confirmation = Checkbox("Confirm move")

        def get_settings(options_json: dict) -> dict:
            return {"move_confirmation": move_confirmation.is_checked()}

        def _set_settings_from_json(settings: dict):
            is_move_confirmed = settings.get("move_confirmation", False)
            if is_move_confirmed:
                move_confirmation.check()
            else:
                move_confirmation.uncheck()

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)

            settings_options = [
                NodesFlow.Node.Option(
                    name="Move Notification",
                    option_component=NodesFlow.WidgetOptionComponent(widget=move_notification),
                ),
                NodesFlow.Node.Option(
                    name="Move Confirmation",
                    option_component=NodesFlow.WidgetOptionComponent(move_confirmation),
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
            need_preview=False,
        )

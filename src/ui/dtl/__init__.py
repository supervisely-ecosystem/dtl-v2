from .actions.base import Action, Layer
from .actions.approx_vector import ApproxVectorAction
from .actions.data import DataAction
from .actions.supervisely import SuperviselyAction
from .actions.dataset import DatasetAction

actions_list = {
    "Data layers": [
        DataAction.name
    ],
    "Transformation layers": [
        ApproxVectorAction.name,
        DatasetAction.name,
    ],
    "Save layers": [
        SuperviselyAction.name,
    ],
}

actions = {
    # Data layers
    DataAction.name: DataAction,
    # Transformation layers
    ApproxVectorAction.name: ApproxVectorAction,
    DatasetAction.name: DatasetAction,
    # Save layers
    SuperviselyAction.name: SuperviselyAction,
}

from .actions.base import Action, Layer
from .actions.data import DataAction
from .actions.approx_vector import ApproxVectorAction
from .actions.bitmap2lines import Bitmap2LinesAction
from .actions.dataset import DatasetAction
from .actions.drop_obj_by_class import DropByClassAction
from .actions.duplicate_objects import DuplicateObjectsAction
from .actions.find_contours import FindContoursAction
from .actions.if_action import IfAction
from .actions.rasterize import RasterizeAction
from .actions.resize import ResizeAction
from .actions.skeletonize import SkeletonizeAction
from .actions.save import SaveAction
from .actions.supervisely import SuperviselyAction
from .actions.save_masks import SaveMasksAction


actions_list = {
    "Data layers": [DataAction.name],
    "Transformation layers": [
        ApproxVectorAction.name,
        Bitmap2LinesAction.name,
        DatasetAction.name,
        DropByClassAction.name,
        DuplicateObjectsAction.name,
        FindContoursAction.name,
        IfAction.name,
        RasterizeAction.name,
        ResizeAction.name,
        SkeletonizeAction.name,
    ],
    "Save layers": [
        SaveAction.name,
        SaveMasksAction.name,
        SuperviselyAction.name,
    ],
}

actions = {
    # Data layers
    DataAction.name: DataAction,
    # Transformation layers
    ApproxVectorAction.name: ApproxVectorAction,
    Bitmap2LinesAction.name: Bitmap2LinesAction,
    DatasetAction.name: DatasetAction,
    DropByClassAction.name: DropByClassAction,
    DuplicateObjectsAction.name: DuplicateObjectsAction,
    FindContoursAction.name: FindContoursAction,
    IfAction.name: IfAction,
    RasterizeAction.name: RasterizeAction,
    ResizeAction.name: ResizeAction,
    SkeletonizeAction.name: SkeletonizeAction,
    # Save layers
    SaveAction.name: SaveAction,
    SaveMasksAction.name: SaveMasksAction,
    SuperviselyAction.name: SuperviselyAction,
}

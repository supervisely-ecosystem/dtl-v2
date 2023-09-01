from .Action import Action
from .actions.data import DataAction
from .actions.approx_vector import ApproxVectorAction
from .actions.background import BackgroundAction
from .actions.bbox import BBoxAction
from .actions.bbox2poly import BboxToPolyAction
from .actions.bitwise_masks import BitwiseMasksAction
from .actions.blur import BlurAction
from .actions.bitmap2lines import Bitmap2LinesAction
from .actions.color_class import ColorClassAction
from .actions.contrast_brightness import ContrastBrightnessAction
from .actions.crop import CropAction
from .actions.dataset import DatasetAction
from .actions.drop_obj_by_class import DropByClassAction
from .actions.drop_lines_by_length import DropLinesByLengthAction
from .actions.drop_noise import DropNoiseAction
from .actions.dummy import DummyAction
from .actions.duplicate_objects import DuplicateObjectsAction
from .actions.find_contours import FindContoursAction
from .actions.flip import FlipAction
from .actions.if_action import IfAction
from .actions.instances_crop import InstancesCropAction
from .actions.line2bitmap import LineToBitmapAction
from .actions.merge_bitmaps import MergeBitmapsAction
from .actions.multiply import MultiplyAction
from .actions.noise import NoiseAction
from .actions.objects_filter import ObjectsFilterAction
from .actions.poly2bitmap import PolygonToBitmapAction
from .actions.random_color import RandomColorsAction
from .actions.rename import RenameAction
from .actions.rasterize import RasterizeAction
from .actions.resize import ResizeAction
from .actions.skeletonize import SkeletonizeAction
from .actions.sliding_window import SlidingWindowAction
from .actions.split_masks import SplitMasksAction
from .actions.tag import TagAction
from .actions.save import SaveAction
from .actions.save_masks import SaveMasksAction
from .actions.supervisely import SuperviselyAction


DATA_ACTIONS = "Data actions"
TRANSFORMATION_ACTIONS = "Transformation actions"
SAVE_ACTIONS = "Save actions"


actions_list = {
    DATA_ACTIONS: [DataAction.name],
    TRANSFORMATION_ACTIONS: [
        ApproxVectorAction.name,
        BackgroundAction.name,
        BBoxAction.name,
        BboxToPolyAction.name,
        Bitmap2LinesAction.name,
        BitwiseMasksAction.name,
        BlurAction.name,
        ColorClassAction.name,
        ContrastBrightnessAction.name,
        CropAction.name,
        DatasetAction.name,
        DropByClassAction.name,
        DropLinesByLengthAction.name,
        DropNoiseAction.name,
        DummyAction.name,
        DuplicateObjectsAction.name,
        FindContoursAction.name,
        FlipAction.name,
        IfAction.name,
        InstancesCropAction.name,
        LineToBitmapAction.name,
        MergeBitmapsAction.name,
        MultiplyAction.name,
        NoiseAction.name,
        ObjectsFilterAction.name,
        PolygonToBitmapAction.name,
        RandomColorsAction.name,
        RasterizeAction.name,
        RenameAction.name,
        ResizeAction.name,
        SkeletonizeAction.name,
        SlidingWindowAction.name,
        SplitMasksAction.name,
        TagAction.name,
    ],
    SAVE_ACTIONS: [
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
    BackgroundAction.name: BackgroundAction,
    BBoxAction.name: BBoxAction,
    BboxToPolyAction.name: BboxToPolyAction,
    Bitmap2LinesAction.name: Bitmap2LinesAction,
    BitwiseMasksAction.name: BitwiseMasksAction,
    BlurAction.name: BlurAction,
    ColorClassAction.name: ColorClassAction,
    ContrastBrightnessAction.name: ContrastBrightnessAction,
    CropAction.name: CropAction,
    DatasetAction.name: DatasetAction,
    DropByClassAction.name: DropByClassAction,
    DropLinesByLengthAction.name: DropLinesByLengthAction,
    DropNoiseAction.name: DropNoiseAction,
    DummyAction.name: DummyAction,
    DuplicateObjectsAction.name: DuplicateObjectsAction,
    FindContoursAction.name: FindContoursAction,
    FlipAction.name: FlipAction,
    IfAction.name: IfAction,
    InstancesCropAction.name: InstancesCropAction,
    LineToBitmapAction.name: LineToBitmapAction,
    MergeBitmapsAction.name: MergeBitmapsAction,
    MultiplyAction.name: MultiplyAction,
    NoiseAction.name: NoiseAction,
    ObjectsFilterAction.name: ObjectsFilterAction,
    PolygonToBitmapAction.name: PolygonToBitmapAction,
    RandomColorsAction.name: RandomColorsAction,
    RasterizeAction.name: RasterizeAction,
    RenameAction.name: RenameAction,
    ResizeAction.name: ResizeAction,
    SkeletonizeAction.name: SkeletonizeAction,
    SlidingWindowAction.name: SlidingWindowAction,
    SplitMasksAction.name: SplitMasksAction,
    TagAction.name: TagAction,
    # Save layers
    SaveAction.name: SaveAction,
    SaveMasksAction.name: SaveMasksAction,
    SuperviselyAction.name: SuperviselyAction,
}

from os.path import realpath, dirname

from src.ui.dtl.utils import get_layer_docs
from src.ui.dtl.actions.other_augs.imgaug_corruptlike.base.imgaug_corruptlike import (
    ImgAugCorruptLikeAction,
)


class ImgAugCorruptlikeColorAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_color"
    title = "iaa.imgcorruptlike Color"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    options = {
        "contrast": "Contrast",
        "brightness": "Brightness",
        "saturate": "Saturate",
    }

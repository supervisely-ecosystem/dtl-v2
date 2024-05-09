from os.path import realpath, dirname

from src.ui.dtl.utils import get_layer_docs
from src.ui.dtl.actions.other_augs.imgaug_corruptlike.base.imgaug_corruptlike import (
    ImgAugCorruptLikeAction,
)


class ImgAugCorruptlikeBlurAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_blur"
    title = "iaa.imgcorruptlike Blur"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    options = {
        "gaussian_blur": "Gaussian Blur",
        "glass_blur": "Glass Blur",
        "defocus_blur": "Defocus Blur",
        "motion_blur": "Motion Blur",
        "zoom_blur": "Zoom Blur",
    }

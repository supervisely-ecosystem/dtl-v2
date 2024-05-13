from os.path import realpath, dirname

from src.ui.dtl.utils import get_layer_docs
from src.ui.dtl.actions.imgaug_augs.corruptlike.base.imgaug_corruptlike import (
    ImgAugCorruptLikeAction,
)


class ImgAugCorruptlikeNoiseAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_noise"
    title = "iaa.imgcorruptlike Noise"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    options = {
        "gaussian_noise": "Gaussian Noise",
        "shot_noise": "Shot Noise",
        "impulse_noise": "Impulse Noise",
        "speckle_noise": "Speckle Noise",
    }

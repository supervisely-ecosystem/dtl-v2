from os.path import realpath, dirname

from src.ui.dtl.utils import get_layer_docs
from src.ui.dtl.actions.other_augs.imgaug_corruptlike.base.imgaug_corruptlike import (
    ImgAugCorruptLikeAction,
)


class ImgAugCorruptlikeWeatherAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_weather"
    title = "iaa.imgcorruptlike Weather"
    description = ""
    md_description = get_layer_docs(dirname(realpath(__file__)))
    options = {
        "fog": "Fog",
        "frost": "Frost",
        "snow": "Snow",
        "spatter": "Spatter",
    }

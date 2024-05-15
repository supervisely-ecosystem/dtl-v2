from typing import Optional

from supervisely.app.widgets import (
    NodesFlow,
    InputNumber,
    Select,
    Field,
)
from src.ui.dtl.Layer import Layer
from src.ui.dtl import ImgAugAugmentationsAction
from os.path import join, exists, realpath, dirname


def get_layer_doc_by_name(doc_name: str) -> str:
    layer_dir = dirname(realpath(__file__))
    md_description = ""
    p = join(layer_dir, doc_name)
    if exists(p):
        with open(p) as f:
            md_description = f.read()
    return md_description


class ImgAugCorruptLikeAction(ImgAugAugmentationsAction):
    name = "iaa_imgaug_corruptlike"
    options = {}

    @classmethod
    def create_new_layer(cls, layer_id: Optional[str] = None):
        options_selector = Select(
            items=[Select.Item(value=v, label=l) for v, l in cls.options.items()],
            size="small",
        )
        options_field = Field(
            title="Augmentation option",
            description="",
            content=options_selector,
        )
        severity_input = InputNumber(value=2, min=1, max=5, step=1, size="small")
        severity_field = Field(
            title="Severity",
            description="",
            content=severity_input,
        )

        def get_settings(options_json: dict) -> dict:
            return {"option": options_selector.get_value(), "severity": severity_input.get_value()}

        def _set_settings_from_json(settings: dict):
            severity = settings.get("severity", 2)
            severity_input.value = severity

            default_option = None
            if len(cls.options) > 0:
                default_option = list(cls.options.keys())[0]
            option = settings.get("option", default_option)
            options_selector.set_value(option)

        def create_options(src: list, dst: list, settings: dict) -> dict:
            _set_settings_from_json(settings)
            settings_options = [
                NodesFlow.Node.Option(
                    name="Augmentation option",
                    option_component=NodesFlow.WidgetOptionComponent(options_field),
                ),
                NodesFlow.Node.Option(
                    name="Severity",
                    option_component=NodesFlow.WidgetOptionComponent(severity_field),
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
            need_preview=True,
        )


class ImgAugCorruptlikeBlurAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_blur"
    title = "iaa.imgcorruptlike Blur"
    description = ""
    md_description = ImgAugCorruptLikeAction.read_md_file(dirname(realpath(__file__)) + "/blur.md")
    options = {
        "defocus_blur": "Defocus Blur",
        "motion_blur": "Motion Blur",
        "zoom_blur": "Zoom Blur",
    }


class ImgAugCorruptlikeColorAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_color"
    title = "iaa.imgcorruptlike Color"
    description = ""
    md_description = ImgAugCorruptLikeAction.read_md_file(dirname(realpath(__file__)) + "/color.md")
    options = {
        "contrast": "Contrast",
        "brightness": "Brightness",
        "saturate": "Saturate",
    }


class ImgAugCorruptlikeCompressionAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_compression"
    title = "iaa.imgcorruptlike Compression"
    docs_url = "https://imgaug.readthedocs.io/en/latest/source/overview/imgcorruptlike.html#elastictransform"
    description = ""
    md_description = ImgAugCorruptLikeAction.read_md_file(
        dirname(realpath(__file__)) + "/compression.md"
    )
    options = {
        "jpeg_compression": "JPEG Compression",
        "pixelate": "Pixelate",
        "elastic_transform": "Elastic Transform",
    }


class ImgAugCorruptlikeNoiseAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_noise"
    title = "iaa.imgcorruptlike Noise"
    description = ""
    md_description = ImgAugCorruptLikeAction.read_md_file(dirname(realpath(__file__)) + "/noise.md")
    options = {
        "gaussian_noise": "Gaussian Noise",
        "shot_noise": "Shot Noise",
        "impulse_noise": "Impulse Noise",
        "speckle_noise": "Speckle Noise",
    }


class ImgAugCorruptlikeWeatherAction(ImgAugCorruptLikeAction):
    name = "iaa_imgcorruptlike_weather"
    title = "iaa.imgcorruptlike Weather"
    description = ""
    md_description = ImgAugCorruptLikeAction.read_md_file(
        dirname(realpath(__file__)) + "/weather.md"
    )
    options = {
        "fog": "Fog",
        "frost": "Frost",
        "snow": "Snow",
        "spatter": "Spatter",
    }

# coding: utf-8

from src.compute.Layer import Layer


class ImgCorruptLikeLayer(Layer):
    action = "iaa_imgaug_corruptlike"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["severity"],
                "properties": {
                    "option": {"type": "string"},
                    "severity": {"type": "integer", "minimum": 1, "maximum": 5},
                },
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def requires_item(self):
        return True

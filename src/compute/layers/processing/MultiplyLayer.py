# coding: utf-8

from src.compute.Layer import Layer


class MultiplyLayer(Layer):
    action = "multiply"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["multiply"],
                "properties": {"multiply": {"type": "integer", "minimum": 1}},
            }
        },
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def process(self, data_el):
        for _ in range(self.settings["multiply"]):
            yield data_el

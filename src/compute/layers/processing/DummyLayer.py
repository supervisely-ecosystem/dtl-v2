# coding: utf-8

from src.compute.Layer import Layer


class DummyLayer(Layer):
    action = 'dummy'

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {}
        }
    }

    def __init__(self, config):
        Layer.__init__(self, config)

    def process(self, data_el):
        yield data_el

# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation


class FilteredProjectLayer(Layer):
    action = "filtered_project"

    layer_settings = {"required": ["settings"], "properties": {"settings": {}}}

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)

    def modifies_data(self):
        return False

    def process(self, data_el):
        yield data_el

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        yield data_els

    def has_batch_processing(self) -> bool:
        return True

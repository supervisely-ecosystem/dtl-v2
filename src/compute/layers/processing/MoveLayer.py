# coding: utf-8

from typing import List, Tuple
from src.compute.dtl_utils.item_descriptor import ImageDescriptor
from src.compute.Layer import Layer
from supervisely import Annotation

import src.globals as g


class MoveLayer(Layer):
    action = "move"

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["move_confirmation"],
                "properties": {"move_confirmation": {"type": "boolean"}},
            }
        },
    }

    def __init__(self, config, net):
        Layer.__init__(self, config, net=net)
        self.entity_ids_to_remove = []

    def validate(self):
        if not self.settings.get("move_confirmation"):
            raise ValueError("Confirm move action on the 'Move' layer card")

    def modifies_data(self):
        return False

    def process(self, data_el):
        yield data_el

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        if self.net.preview_mode:
            yield data_els
        else:
            item_descs, anns = zip(*data_els)
            for item in item_descs:
                item: ImageDescriptor
                self.entity_ids_to_remove.append(item.info.item_info.id)
            yield tuple(zip(item_descs, anns))

    def postprocess(self):
        g.api.image.remove_batch(self.entity_ids_to_remove)
        # need to remove ids from g.FILTERED_IDS?

    def has_batch_processing(self) -> bool:
        return True

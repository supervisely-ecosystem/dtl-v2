# coding: utf-8
from typing import Tuple

from supervisely import Annotation

from src.compute.Layer import Layer
from src.compute.dtl_utils.image_descriptor import ImageDescriptor


class FlipLayer(Layer):

    action = 'flip'

    layer_settings = {
        "required": ["settings"],
        "properties": {
            "settings": {
                "type": "object",
                "required": ["axis"],
                "properties": {
                    "axis": {
                        "type": "string",
                        "enum": ["horizontal", "vertical"]
                    }
                }
            }
        }
    }

    def __init__(self, config):
        Layer.__init__(self, config)
        self.horiz = self.settings['axis'] == 'horizontal'

    def requires_image(self):
        return True

    def process(self, data_el: Tuple[ImageDescriptor, Annotation]):
        img_desc, ann = data_el
        img = img_desc.read_image()

        if self.horiz:
            img = img[::-1, :, :]
        else:
            img = img[:, ::-1, :]

        new_img_desc = img_desc.clone_with_img(img)
        new_labels = []
        for label in ann.labels:
            if self.horiz:
                new_label = label.clone(geometry=label.geometry.flipud(ann.img_size))
            else:
                new_label = label.clone(geometry=label.geometry.fliplr(ann.img_size))
            new_labels.append(new_label)
        ann = ann.clone(labels=new_labels)

        yield new_img_desc, ann

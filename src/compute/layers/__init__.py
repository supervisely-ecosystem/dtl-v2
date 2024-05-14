import inspect
import pkgutil

from src.compute.Layer import Layer

from src.compute.layers import data
from src.compute.layers import processing
from src.compute.layers import save


def register_layers(package, type):
    prefix = package.__name__ + "."
    registered_classes = set()

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        module = __import__(modname, fromlist="dummy")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Layer) and obj != Layer:
                if obj not in registered_classes:
                    Layer.register_layer(obj, type)
                    registered_classes.add(obj)


register_layers(data, "data")
register_layers(processing, "processing")
register_layers(save, "save")

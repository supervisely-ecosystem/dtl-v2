import inspect
import pkgutil

from src.compute.Layer import Layer

from src.compute.layers import data
from src.compute.layers import processing
from src.compute.layers import save


def register_layers(package, type):
    prefix = package.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        module = __import__(modname, fromlist="dummy")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if issubclass(obj, Layer) and obj != Layer:
                    Layer.register_layer(obj, type)


register_layers(data, 'data')
register_layers(processing, 'processing')
register_layers(save, 'save')

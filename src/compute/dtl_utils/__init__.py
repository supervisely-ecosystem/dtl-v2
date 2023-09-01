from supervisely import Annotation


def apply_to_labels(ann: Annotation, fn):
    """fn must receive a single argument of type Label and return iterable of labels"""
    new_labels = []
    for label in ann.labels:
        new_labels.extend(fn(label))
    ann = ann.clone(labels=new_labels)
    return ann
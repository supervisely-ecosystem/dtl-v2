from supervisely.app.widgets import NodesFlow


class Action:
    name = None
    title = None

    @classmethod
    def create_options(cls):
        raise NotImplementedError
    
    @classmethod
    def create_inputs(cls):
        return [NodesFlow.Node.Input("source", "Source")]
    
    @classmethod
    def create_outputs(cls):
        return [NodesFlow.Node.Output("destination", "Destination")]


class Layer:
    def __init__(self, action: Action):
        self.action = action

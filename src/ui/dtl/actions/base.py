from supervisely.app.widgets import NodesFlow, Container, Text


class Action:
    name = None
    title = None
    docs_url = None
    description = None
    width = 200

    @classmethod
    def create_options(cls):
        raise NotImplementedError

    @classmethod
    def create_inputs(cls):
        return [NodesFlow.Node.Input("source", "Source")]

    @classmethod
    def create_outputs(cls):
        return [NodesFlow.Node.Output("destination", "Destination")]

    @classmethod
    def create_info_widget(cls):
        return Container(
            widgets=[
                Text(f"<h3>{cls.title}</h3>", color="white"),
                Text(
                    f'<a href="{cls.docs_url}" target="_blank" style="color: white;">Docs</a>'
                ),
                Text(f"<p>{cls.description}</p>", color="white"),
            ]
        )

    @classmethod
    def parse_options(cls, options: dict) -> dict:
        return {
            "src": [],
            "dst": [],
            "settings": {},
        }


class Layer:
    def __init__(self, action: Action):
        self.action = action

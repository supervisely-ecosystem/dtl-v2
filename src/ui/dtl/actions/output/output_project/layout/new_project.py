from supervisely.app.widgets import Text, Input, Container
from src.ui.dtl.utils import get_text_font_size


def create_new_project_widgets():
    new_project_name_text = Text("Project name", status="text", font_size=get_text_font_size())
    new_project_name_input = Input(value="", placeholder="Enter project name", size="small")
    new_project_container = Container([new_project_name_text, new_project_name_input])
    return new_project_name_text, new_project_name_input, new_project_container

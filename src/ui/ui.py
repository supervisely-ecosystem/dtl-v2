from supervisely.app.widgets import Tabs, Container, Flexbox, Button, Dialog

from src.ui.tabs.configure import layout as configure_tab_layout
from src.ui.tabs.presets import save_layout, load_layout
from src.ui.tabs.run import layout as run_layout
from src.globals import error_dialog
from src.ui.dtl.utils import get_set_settings_button_style

# tabs = Tabs(
#     labels=["Configure Nodes", "JSON Preview", "Run"],
#     contents=[configure_tab_layout, presets_layout, run_layout],
# )
# layout = Container([tabs, error_dialog])

run_dialog = Dialog(title="Run", content=run_layout)
run_button = Button(
    "Run",
    icon="zmdi zmdi-play",
    button_size="small",
    style="border: 1px solid rgb(191, 203, 217); color: black; background-color: white; margin: 10px 10px 10px 40px;",
)

save_dialog = Dialog(title="Save Preset", content=save_layout)
save_button = Button(
    "", icon="zmdi zmdi-floppy", button_size="large", button_type="text", style="color: black;"
)

load_dialog = Dialog(title="Load Preset", content=load_layout)
load_button = Button(
    "",
    icon="zmdi zmdi-cloud-download",
    button_size="large",
    button_type="text",
    style="color: black;",
)

buttons = Flexbox(widgets=[run_button, save_button, load_button])

layout = Container(
    widgets=[error_dialog, run_dialog, save_dialog, load_dialog, buttons, configure_tab_layout],
    gap=0,
)


@run_button.click
def show_run_dialog():
    run_dialog.show()


@save_button.click
def save_presets_dialog():
    save_dialog.show()


@load_button.click
def load_presets_dialog():
    load_dialog.show()

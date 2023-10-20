from supervisely.app.widgets import Container, Flexbox, Button, Dialog

from src.ui.tabs.configure import layout as configure_tab_layout
from src.ui.tabs.presets import (
    update_load_dialog,
    save_dialog,
    load_dialog,
)
from src.ui.tabs.run import layout as run_layout
from src.globals import error_dialog

run_dialog = Dialog(title="Run", content=run_layout)
run_button = Button(
    "Run",
    icon="zmdi zmdi-play",
    button_size="small",
    style="border: 1px solid rgb(191, 203, 217); color: black; background-color: white; margin: 10px 10px 10px 40px;",
)

save_button = Button("save", icon="zmdi zmdi-floppy", button_size="large", button_type="text")

load_button = Button(
    "load",
    icon="zmdi zmdi-cloud-download",
    button_size="large",
    button_type="text",
)

header = Flexbox(widgets=[run_button, save_button, load_button])

layout = Container(
    widgets=[error_dialog, run_dialog, save_dialog, load_dialog, configure_tab_layout],
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
    update_load_dialog()

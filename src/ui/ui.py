from supervisely.app.widgets import Tabs, Container

from src.ui.tabs.configure import layout as configure_tab_layout
from src.ui.tabs.json_preview import layout as json_preview_layout
from src.ui.tabs.run import layout as run_layout
from src.globals import error_dialog

tabs = Tabs(
    labels=["Configure Nodes", "JSON Preview", "Run"],
    contents=[configure_tab_layout, json_preview_layout, run_layout],
)
layout = Container([tabs, error_dialog])

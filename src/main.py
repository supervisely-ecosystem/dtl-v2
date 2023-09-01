import shutil
import os
from supervisely import Application

from src.ui.ui import layout
import src.globals as g

shutil.rmtree(g.STATIC_DIR, ignore_errors=True)
os.mkdir(g.STATIC_DIR)
app = Application(layout=layout, static_dir=g.STATIC_DIR)

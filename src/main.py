import threading
import time
from supervisely import Application

from src.ui.ui import layout, header
from src.ui.tabs.configure import update_metas, update_nodes
from src.ui.tabs.presets import apply_json
import src.globals as g
import src.utils as u

u.clean_static_dir(g.STATIC_DIR)

app = Application(layout=layout, static_dir=g.STATIC_DIR, session_info_extra_content=header)


def _update_f():
    while True:
        updates = []
        while not g.update_queue.empty():
            updates.append(g.update_queue.get())
        if len(updates) == 0:
            time.sleep(0.1)
            continue
        try:
            if "load_json" in updates:
                apply_json()
            elif "nodes" in updates:
                update_nodes()
            else:
                update_metas()
        finally:
            for _ in range(len(updates)):
                g.update_queue.task_done()
        time.sleep(0.1)


update_loop = threading.Thread(
    target=_update_f,
    name="App update loop",
    daemon=True,
)

update_loop.start()

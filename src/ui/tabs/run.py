from pathlib import Path

from supervisely.app.widgets import Button, Container, Progress, Text, ReloadableArea, Empty
from supervisely.app import show_dialog
from supervisely.io.fs import get_file_size
import supervisely as sly

from src.compute.main import main as compute_dtls
from src.compute.layers.save.SuperviselyLayer import SuperviselyLayer
from src.ui.tabs.configure import nodes_flow
import src.utils as utils
import src.ui.utils as ui_utils
import src.globals as g
from src.exceptions import CustomException, handle_exception


run_btn = Button("Run", icon="zmdi zmdi-play")
progress = Progress(hide_on_finish=False)
download_archives_urls = Text("")
results = ReloadableArea(Empty())
results.hide()

layout = Container(widgets=[run_btn, progress, download_archives_urls, results])


@run_btn.click
@handle_exception
def run():
    edges = nodes_flow.get_edges_json()
    nodes_state = nodes_flow.get_nodes_state_json()

    run_btn.hide()
    results.hide()
    progress(message="Running...", total=1)
    progress.show()

    try:
        # init layers
        ui_utils.init_layers(nodes_state)

        # init layers sources
        # destinations are defined in init_layers
        ui_utils.init_src(edges)

        # prepare results dir
        utils.delete_results_dir()
        utils.create_results_dir()
        utils.delete_data_dir()
        utils.create_data_dir()

        # Run
        dtl_json = [g.layers[node_id].to_json() for node_id in nodes_state]
        utils.save_dtl_json(dtl_json)
        net = compute_dtls(progress)

        # Save results
        file_infos = []
        pr_dirs = [p for p in Path(g.RESULTS_DIR).iterdir() if p.is_dir()]
        for i, pr_dir in enumerate(pr_dirs):
            with progress(
                message=[f'[{i+1}/{len(pr_dirs)}] Archiving result project "{pr_dir.name}"'],
                total=1,
            ) as pbar:
                tar_path = str(pr_dir) + ".tar"
                sly.fs.archive_directory(pr_dir, tar_path)
                pbar.update(1)
            with progress(
                message=f'[{i+1}/{len(pr_dirs)}] Uploading result project "{pr_dir.name}"',
                unit="B",
                unit_scale=True,
                total=get_file_size(tar_path),
            ) as pbar:
                file_info = g.api.file.upload(
                    g.TEAM_ID,
                    src=tar_path,
                    dst=f"/dtl/{utils.get_task()}/{Path(tar_path).name}",
                    progress_cb=pbar,
                )
            file_infos.append(file_info)
            if not sly.is_development():
                g.api.task.set_output_archive(sly.env.task_id(), file_info.id, file_info.name)

        supervisely_layers = [l for l in net.layers if isinstance(l, SuperviselyLayer)]
        results.set_content(ui_utils.create_results_widget(file_infos, supervisely_layers))
        results.reload()
        results.show()
    except CustomException as e:
        ui_utils.show_error("Error", e)
        raise e
    except Exception as e:
        show_dialog("Error", description=f"Unexpected Error: {str(e)}", status="error")
        raise e
    finally:
        progress.hide()
        run_btn.show()

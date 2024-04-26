# coding: utf-8
from time import time
from typing import Tuple, Union, List

from supervisely import Annotation, VideoAnnotation, KeyIdMap, logger
import supervisely.io.fs as sly_fs
import supervisely.io.json as sly_json
from src.compute.dtl_utils.item_descriptor import ImageDescriptor, VideoDescriptor
from src.compute.Layer import Layer
from src.exceptions import GraphError
import src.globals as g
from supervisely.io.fs import get_file_ext


def _get_source_projects_ids_from_dtl():
    source_projects_ids = []
    for action in g.current_dtl_json:
        if action["action"] == "images_project" or action["action"] == "videos_project":
            if len(action["src"]) == 0:
                continue
            project_name = action["src"][0].split("/")[0]
            project_id = g.api.project.get_info_by_name(g.WORKSPACE_ID, project_name).id
            source_projects_ids.append(project_id)
    return source_projects_ids


class CreateNewProjectLayer(Layer):
    action = "create_new_project"
    legacy_action = "supervisely"

    layer_settings = {"required": ["settings"], "properties": {"settings": {}}}

    def __init__(self, config, output_folder, net):
        Layer.__init__(self, config, net=net)
        self.output_folder = output_folder
        self.sly_project_info = None

    def validate_dest_connections(self):
        for dst in self.dsts:
            if len(dst) == 0:
                raise ValueError("Destination name in '{}' layer is empty!".format(self.action))

    def modifies_data(self):
        return False

    def preprocess(self):
        if self.net.preview_mode:
            return
        if self.output_meta is None:
            raise GraphError(
                "Output meta is not set. Check that node is connected", extra={"layer": self.action}
            )
        if len(self.dsts) == 0:
            raise GraphError(
                "Enter name for the output project to the input field in the 'Create New Project' layer"
            )
        dst = self.dsts[0]
        self.out_project_name = dst

        self.sly_project_info = g.api.project.create(
            g.WORKSPACE_ID,
            self.out_project_name,
            type=self.net.modality,
            change_name_if_conflict=True,
        )
        g.api.project.update_meta(self.sly_project_info.id, self.output_meta)

        custom_data = {
            "source_projects": _get_source_projects_ids_from_dtl(),
            "data-nodes": g.current_dtl_json,
        }
        g.api.project.update_custom_data(self.sly_project_info.id, custom_data)

    def get_or_create_dataset(self, dataset_name):
        if not g.api.dataset.exists(self.sly_project_info.id, dataset_name):
            return g.api.dataset.create(self.sly_project_info.id, dataset_name)
        else:
            return g.api.dataset.get_info_by_name(self.sly_project_info.id, dataset_name)

    def process(
        self,
        data_el: Tuple[Union[ImageDescriptor, VideoDescriptor], Union[Annotation, VideoAnnotation]],
    ):
        item_desc, ann = data_el

        if not self.net.preview_mode:
            dataset_name = item_desc.get_res_ds_name()
            out_item_name = (
                self.get_free_name(item_desc.get_item_name(), dataset_name, self.out_project_name)
                + item_desc.get_item_ext()
            )
            if self.sly_project_info is not None:
                dataset_info = self.get_or_create_dataset(dataset_name)
                if self.net.modality == "images":
                    if self.net.may_require_items():
                        item_info = g.api.image.upload_np(
                            dataset_info.id, out_item_name, item_desc.read_image()
                        )
                    else:
                        item_info = g.api.image.upload_id(
                            dataset_info.id, out_item_name, item_desc.info.item_info.id
                        )
                    g.api.annotation.upload_ann(item_info.id, ann)
                elif self.net.modality == "videos":
                    video_info = g.api.video.upload_path(
                        dataset_info.id, out_item_name, item_desc.item_data
                    )
                    ann_path = f"{item_desc.item_data}.json"
                    if not sly_fs.file_exists(ann_path):
                        ann_json = ann.to_json(KeyIdMap())
                        sly_json.dump_json_file(ann_json, ann_path)
                    g.api.video.annotation.upload_paths(
                        [video_info.id], [ann_path], self.output_meta
                    )
                    # sly_fs.silent_remove(item_desc.item_data)
                    # sly_fs.silent_remove(ann_path)

        yield ([item_desc, ann])

    def process_batch(self, data_els: List[Tuple[ImageDescriptor, Annotation]]):
        if self.net.preview_mode:
            yield data_els
        else:
            logger.debug("Process CreateNewProjectLayer")
            start_time_whole = time()

            logger.debug("CreateNewProjectLayer: PROCESS ITEMS BEFORE UPLOAD")
            start_time = time()
            item_descs, anns = zip(*data_els)
            ds_item_map = {}
            for item_desc, ann in zip(item_descs, anns):
                dataset_name = item_desc.get_res_ds_name()
                if dataset_name not in ds_item_map:
                    ds_item_map[dataset_name] = []
                ds_item_map[dataset_name].append((item_desc, ann))

            for ds_name in ds_item_map:
                out_item_names = [
                    self.get_free_name(
                        item_desc.get_item_name(), dataset_name, self.out_project_name
                    )
                    + get_file_ext(item_desc.info.item_info.name)
                    for item_desc, _ in ds_item_map[ds_name]
                ]
                if self.sly_project_info is not None:
                    dataset_info = self.get_or_create_dataset(ds_name)

                    end_time = time()
                    logger.debug(
                        f"CreateNewProjectLayer: PROCESS ITEMS BEFORE UPLOAD time: '{end_time - start_time}' sec"
                    )
                    if self.net.modality == "images":
                        if self.net.may_require_items():
                            item_infos = g.api.image.upload_nps(
                                dataset_info.id,
                                out_item_names,
                                [item_desc.read_image() for item_desc, _ in ds_item_map[ds_name]],
                            )
                        else:
                            logger.debug("CreateNewProjectLayer: upload_ids")
                            upload_start_time = time()
                            item_infos = g.api.image.upload_ids(
                                dataset_info.id,
                                out_item_names,
                                [
                                    item_desc.info.item_info.id
                                    for item_desc, _ in ds_item_map[ds_name]
                                ],
                            )
                            upload_end_time = time()
                            logger.debug(
                                f"CreateNewProjectLayer: upload_ids time: '{upload_end_time - upload_start_time}' sec"
                            )

                        logger.debug("CreateNewProjectLayer: upload_anns")
                        upload_anns_start_time = time()
                        g.api.annotation.upload_anns(
                            [item_info.id for item_info in item_infos],
                            [ann for _, ann in ds_item_map[ds_name]],
                        )
                        upload_anns_end_time = time()
                        logger.debug(
                            f"CreateNewProjectLayer: upload_anns time: '{upload_anns_end_time - upload_anns_start_time}' sec"
                        )

                    elif self.net.modality == "videos":
                        item_infos = g.api.video.upload_paths(
                            dataset_info.id,
                            out_item_names,
                            [item_desc.item_data for item_desc, _ in ds_item_map[ds_name]],
                        )
                        ann_paths = [
                            f"{item_desc.item_data}.json" for item_desc, _ in ds_item_map[ds_name]
                        ]
                        for ann, ann_path, video_info in zip(
                            [ann for _, ann in ds_item_map[ds_name]], ann_paths, item_infos
                        ):
                            if not sly_fs.file_exists(ann_path):
                                ann_json = ann.to_json(KeyIdMap())
                                sly_json.dump_json_file(ann_json, ann_path)
                            g.api.video.annotation.upload_paths(
                                [video_info.id], [ann_path], self.output_meta
                            )

            end_time_whole = time()
            logger.debug(
                f"CreateNewProjectLayer process_batch time: '{end_time_whole - start_time_whole}' sec"
            )
            yield tuple(zip(item_descs, anns))

    def has_batch_processing(self):
        return True

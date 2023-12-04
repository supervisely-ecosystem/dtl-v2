# coding: utf-8

import os
import os.path as osp

from src.compute.utils.json_utils import json_load, json_dump
from supervisely import ProjectMeta
from src.compute.dtl_utils.dtl_paths import DtlPaths

import src.globals as g


class DtlHelper:
    def __init__(self):
        self.paths = DtlPaths()
        self.graph = json_load(self.paths.graph_path)
        self.modality = None

        self.in_project_metas = {}
        self.in_project_dirs = {}
        for pr_dir in self.paths.project_dirs:
            pr_name = os.path.basename(pr_dir)
            self.in_project_metas[pr_name] = meta_from_dir(pr_dir)
            self.in_project_dirs[pr_name] = pr_dir
            if self.modality is None:
                self.modality = self.in_project_metas[pr_name].project_type.name
            if self.modality != self.in_project_metas[pr_name].project_type.name:
                raise RuntimeError("All projects must have same data type (modality)")
            if self.modality not in g.SUPPORTED_MODALITIES:
                raise RuntimeError("Data type (modality) must be images or videos")

    def save_res_meta(self, meta):
        json_dump(meta.to_json(), self.paths.res_meta_path)


def meta_from_dir(dir_path):
    fpath = osp.join(dir_path, "meta.json")
    if not osp.exists(fpath) or not osp.isfile(fpath):
        raise RuntimeError("File with meta not found in dir: {}".format(dir_path))
    return ProjectMeta.from_json(json_load(fpath))

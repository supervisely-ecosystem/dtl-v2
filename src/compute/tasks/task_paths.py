# coding: utf-8

import os
import os.path as osp


class TaskPaths:
    def __init__(self, determine_in_project=True, task_dir='/sly_task_data'):
        self._task_dir = task_dir
        self._settings_path = osp.join(task_dir, 'task_settings.json')
        self._model_dir = osp.join(task_dir, 'model')
        self._results_dir = osp.join(task_dir, 'results')
        self._data_dir = osp.join(task_dir, 'data')
        self._debug_dir = osp.join(task_dir, 'tmp')

        if not determine_in_project:
            self._project_dir = None
        else:
            data_subfolders = [f.path for f in os.scandir(self._data_dir) if f.is_dir()]
            if len(data_subfolders) == 0:
                raise RuntimeError('Data folder is empty.')
            elif len(data_subfolders) > 1:
                raise NotImplementedError('Work with multiple projects is not supported yet.')
            self._project_dir = data_subfolders[0]

    @property
    def task_dir(self):
        return self._task_dir

    @property
    def settings_path(self):
        return self._settings_path

    @property
    def model_dir(self):
        return self._model_dir

    @staticmethod
    def model_config_name():
        return 'config.json'

    @property
    def model_config_fpath(self):
        return osp.join(self._model_dir, self.model_config_name())

    @property
    def results_dir(self):
        return self._results_dir

    @property
    def project_dir(self):
        return self._project_dir

    @property
    def debug_dir(self):
        return self._debug_dir

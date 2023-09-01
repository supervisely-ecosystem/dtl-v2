# coding: utf-8

from collections import defaultdict


def get_data_sources(graph_json):
    all_ds_marker = '*'
    data_sources = defaultdict(set)
    for layer in graph_json:
        if layer['action'] == 'data':
            for src in layer['src']:
                src_parts = src.split('/')
                src_project_name = src_parts[0]
                src_dataset_name = src_parts[1] if len(src_parts) > 1 else all_ds_marker
                data_sources[src_project_name].add(src_dataset_name)

    def _squeeze_datasets(datasets):
        if all_ds_marker in datasets:
            res = all_ds_marker
        else:
            res = list(datasets)
        return res

    data_sources = {k: _squeeze_datasets(v) for k, v in data_sources.items()}
    return data_sources


def get_res_project_name(graph_json):
    for layer in graph_json:
        if layer['action'] in ['supervisely', 'save', 'save_masks']:
            return layer['dst']
    raise RuntimeError('Supervisely save layer not found.')

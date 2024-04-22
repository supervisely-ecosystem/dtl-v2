import pandas as pd
from typing import List
from supervisely import Api, ImageInfo


def build_filtered_table(api: Api, project_id: int, filtered_items_ids: List[int]) -> pd.DataFrame:
    datasets = api.dataset.get_list(project_id)
    datasets_map = {ds.id: ds.name for ds in datasets}

    all_item_infos = []
    for dataset in datasets:
        item_list = api.image.get_list(dataset.id)
        # for images
        all_item_infos.extend(item_list)

    filtered_item_infos = [
        item_info for item_info in all_item_infos if item_info.id in filtered_items_ids
    ]

    columns = ["Name", "Dataset", "Shape (WxH)", "Classes", "Tags"]
    data = []
    for item_info in filtered_item_infos:
        # for images
        item_info: ImageInfo
        item_data = []
        item_data.append(item_info.name)
        item_data.append(datasets_map[item_info.dataset_id])
        item_data.append(f"{item_info.width}x{item_info.height}")
        item_data.append(item_info.labels_count)
        item_data.append(len(item_info.tags))
        data.append(item_data)

    dataframe = pd.DataFrame(data=data, columns=columns)
    return dataframe

import pandas as pd
from typing import List
from supervisely import Api, ImageInfo


def build_filtered_table(
    api: Api, project_id: int, filtered_items: List[ImageInfo]
) -> pd.DataFrame:
    datasets = api.dataset.get_list(project_id)
    datasets_map = {ds.id: ds.name for ds in datasets}

    columns = ["Name", "Dataset", "Shape (WxH)", "Classes", "Tags"]
    data = []
    for item_info in filtered_items:
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

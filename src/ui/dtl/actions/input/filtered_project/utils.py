import pandas as pd
from typing import List
from supervisely import Api, ImageInfo


def build_filtered_table(api: Api, project_id: int, filtered_items_ids: List[int]) -> pd.DataFrame:
    datasets = api.dataset.get_list(project_id)
    datasets_map = {ds.id: ds.name for ds in datasets}

    columns = ["Name", "Dataset", "Shape (WxH)", "Classes", "Tags"]
    image_infos = [api.image.get_info_by_id(image_id) for image_id in filtered_items_ids]
    data = []
    for image_info in image_infos:
        image_info: ImageInfo
        image_data = []
        # image_info: ImageInfo
        image_data.append(image_info.name)
        image_data.append(datasets_map[image_info.dataset_id])
        image_data.append(f"{image_info.width}x{image_info.height}")
        image_data.append(image_info.labels_count)
        image_data.append(len(image_info.tags))
        data.append(image_data)

    dataframe = pd.DataFrame(data=data, columns=columns)
    return dataframe

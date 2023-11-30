# coding: utf-8

from typing import NamedTuple
import cv2
import numpy as np

from supervisely.api.image_api import ImageInfo
from supervisely.api.video.video_api import VideoInfo
from supervisely.api.project_api import ProjectInfo
from supervisely.api.dataset_api import DatasetInfo


from src.compute.utils.os_utils import ensure_base_path


class ItemDescriptor:
    def __init__(self, info: NamedTuple, modify_ds_name: bool = True):
        self.info = info
        self.item_data = None  # can be changed in comp graph
        self.info = info
        if modify_ds_name:
            self.res_ds_name = "{}__{}".format(self.info.project_name, self.info.ds_name)
        else:
            self.res_ds_name = self.info.ds_name

    def read_item(self) -> None:
        raise NotImplementedError

    def update_item(self, item) -> None:
        self.item_data = item

    # def write_item_local(self, item_path) -> None:
    #     raise NotImplementedError

    # def encode_item(self) -> None:
    #     raise NotImplementedError

    def need_write(self) -> bool:
        if self.item_data is None:
            return False
        return True

    def get_res_ds_name(self) -> str:
        return self.res_ds_name

    def get_pr_name(self) -> str:
        return self.info.project_name

    def get_ds_name(self) -> str:
        return self.info.ds_name

    def get_item_name(self) -> str:
        return self.info.item_name

    def get_item_ext(self) -> str:
        return self.info.ia_data["item_ext"]

    def get_item_path(self) -> str:
        return self.info.item_path

    def set_item_name(self, new_name) -> None:
        self.info.item_name = new_name

    def clone_with_item(self, new_item):
        new_obj = self.__class__(self.info)
        new_obj.item_data = new_item
        new_obj.res_ds_name = self.res_ds_name
        return new_obj

    def clone_with_name(self, new_name) -> None:
        self.info: NamedTuple
        new_info = self.info._replace(item_name=new_name)
        new_obj = self.__class__(new_info)
        new_obj.item_data = self.item_data
        new_obj.res_ds_name = self.res_ds_name
        return new_obj


class ImageDescriptor(ItemDescriptor):
    def __init__(self, info: ImageInfo, modify_ds_name: bool = True) -> None:
        super().__init__(info, modify_ds_name)

    def read_image(self) -> np.ndarray:
        if self.item_data is not None:
            return self.item_data

        img = cv2.imread(self.info.item_path)
        if img is None:
            raise RuntimeError("Image not found. {}".format(self.info.item_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def write_image_local(self, img_path) -> None:
        if self.item_data is None:
            raise RuntimeError(
                "ImageDescriptor [write_image_local] item_data is None:{}".format(img_path)
            )
        img_res = self.item_data.astype(np.uint8)
        img_res = cv2.cvtColor(img_res, cv2.COLOR_RGB2BGR)
        ensure_base_path(img_path)
        cv2.imwrite(img_path, img_res)

    def encode_image(self) -> bytes:
        if self.item_data is None:
            raise RuntimeError("ImageDescriptor [encode_image] item_data is None.")
        img_res = self.item_data.astype(np.uint8)
        img_res = cv2.cvtColor(img_res, cv2.COLOR_RGB2BGR)
        res_bytes = cv2.imencode(".png", img_res)[1]
        return res_bytes


class VideoDescriptor(ItemDescriptor):
    def __init__(self, info: VideoInfo, modify_ds_name: bool = True):
        super().__init__(info, modify_ds_name)

    def read_video(self) -> cv2.VideoCapture:
        if self.item_data is not None:
            return self.item_data
        video = cv2.VideoCapture(self.get_item_path())
        if not video.isOpened():
            raise RuntimeError("Video not found. {}".format(self.get_item_path()))
        self.item_data = video
        return video

    def write_video_local(self, video_path):
        if self.item_data is None:
            raise RuntimeError("No video data available to write.")

        frame_rate = None
        video_shape = None
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        video = cv2.VideoWriter(video_path, fourcc, frame_rate, video_shape)
        for frame in self.item_data:
            video.write(frame)  # Writing the frame
        video.release()

    def encode_video(self):
        if self.item_data is None:
            raise RuntimeError("No video data available to encode.")

        import io

        buffer = io.BytesIO()
        frame_rate = None
        video_shape = None
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        video = cv2.VideoWriter(self.item_data, fourcc, frame_rate, video_shape)
        for frame in self.item_data:
            video.write(frame)  # Writing the frame
        video.release()
        buffer.seek(0)
        return buffer.getvalue()

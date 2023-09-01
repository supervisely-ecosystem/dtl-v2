# coding: utf-8

import os
import os.path as osp
import base64
import functools

import cv2
import numpy as np
import skimage.transform
from PIL import Image


# dsize as WxH
# designed to replace cv2.resize INTER_NEAREST
# works with different dtypes and number of channels; speed isn't guaranteed
def resize_inter_nearest(src_img, dsize=None, fx=0, fy=0):
    if dsize is not None:
        target_shape = (dsize[1], dsize[0])
    else:
        target_shape = (np.round(fy * src_img.shape[0]), np.round(fx * src_img.shape[1]))

    if target_shape[0] <= 0 or target_shape[1] <= 0:
        raise RuntimeError("Wrong resize parameters.")

    res = skimage.transform.resize(
        src_img, target_shape, order=0, preserve_range=True, mode="constant"
    ).astype(src_img.dtype)
    return res


class ImgProto:
    @classmethod
    def img2str(cls, img):
        encoded = cv2.imencode(".png", img)[1].tostring()
        return base64.b64encode(encoded).decode("utf-8")

    # np.uint8, original shape
    @classmethod
    def str2img_original(cls, s):
        n = np.fromstring(base64.b64decode(s), np.uint8)
        imdecoded = cv2.imdecode(n, cv2.IMREAD_UNCHANGED)
        res = imdecoded.astype(np.uint8)
        return res

    # np.uint8, alpha channel from color image or source single channel
    @classmethod
    def str2img_single_channel(cls, s):
        imdecoded = cls.str2img_original(s)
        if (len(imdecoded.shape) == 3) and (imdecoded.shape[2] >= 4):
            mask = imdecoded[:, :, 3]  # 4-channel imgs
        elif len(imdecoded.shape) == 2:
            mask = imdecoded  # flat 2d mask
        else:
            raise RuntimeError("Wrong internal mask format.")
        return mask


# with np.uint8; for visualization; considers black fg as transparent
def overlay_images(bkg_img, fg_img, fg_coeff):
    comb_img = (fg_coeff * fg_img + (1 - fg_coeff) * bkg_img).astype(np.uint8)

    black_mask = (fg_img[:, :, 0] == 0) & (fg_img[:, :, 1] == 0) & (fg_img[:, :, 2] == 0)
    comb_img[black_mask] = bkg_img[black_mask]
    comb_img = np.clip(comb_img, 0, 255)

    return comb_img


class ImportVideoLister:
    _included_extensions = [
        "avi",
        "mp4",
    ]
    extensions = {"." + x for x in _included_extensions + [x.upper() for x in _included_extensions]}

    @classmethod
    def list_videos(cls, dir_):
        fnames = (f.name for f in os.scandir(dir_) if f.is_file())
        video_names = list(filter(lambda x: osp.splitext(x)[1] in cls.extensions, fnames))
        return video_names


class ImportImgLister:
    _included_extensions = [
        "jpg",
        "jpeg",
        "bmp",
        "png",
    ]
    extensions = {"." + x for x in _included_extensions + [x.upper() for x in _included_extensions]}

    @classmethod
    def list_images(cls, dir_):
        fnames = (f.name for f in os.scandir(dir_) if f.is_file())
        img_names = list(filter(lambda x: osp.splitext(x)[1] in cls.extensions, fnames))
        return img_names


# https://stackoverflow.com/a/30462851
def image_transpose_exif(im):
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.

    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [  # Val  0th row  0th col
        [],  #  0    (reserved)
        [],  #  1   top      left
        [Image.FLIP_LEFT_RIGHT],  #  2   top      right
        [Image.ROTATE_180],  #  3   bottom   right
        [Image.FLIP_TOP_BOTTOM],  #  4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  #  5   left     top
        [Image.ROTATE_270],  #  6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  #  7   right    bottom
        [Image.ROTATE_90],  #  8   left     bottom
    ]

    seq = exif_transpose_sequences[im._getexif()[exif_orientation_tag]]
    return functools.reduce(type(im).transpose, seq, im)


def drop_image_alpha_channel(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


# coding: utf-8

import cv2
import numpy as np


class ImageResizer:
    def _determine_resize_params(self, src_size_hw, res_size_hw, keep):
        h, w = src_size_hw
        res_height, res_width = res_size_hw
        if keep:
            if res_height == -1:
                scale = res_width / w
                new_h = int(round(h * scale))
                new_w = res_width
            elif res_width == -1:
                scale = res_height / h
                new_h = res_height
                new_w = int(round(w * scale))
            else:
                scale = min(res_height / h, res_width / w)
                new_h = res_height
                new_w = res_width

            self._resize_args = [None]
            self._resize_kwargs = {"fx": scale, "fy": scale}
            self._scale_x, self._scale_y = scale, scale
            left, top = (new_w - np.round(scale * w).astype("int")) // 2, (
                new_h - np.round(scale * h).astype("int")
            ) // 2
        else:
            self._scale_x, self._scale_y = res_width / w, res_height / h
            self._resize_args = [(res_width, res_height)]
            self._resize_kwargs = {}
            new_h, new_w = res_height, res_width
            left, top = 0, 0
        self.new_h, self.new_w = new_h, new_w
        self._left, self._top = left, top

    def __init__(self, src_size_hw, res_size_hw, keep=False):
        self.src_size_hw = tuple(src_size_hw)
        self._determine_resize_params(src_size_hw, res_size_hw, keep)

    def _get_res_image_shape(self, img):
        if len(img.shape) > 2:
            res_shape = (self.new_h, self.new_w, img.shape[2])
        else:
            res_shape = (self.new_h, self.new_w)
        return res_shape

    def resize_img(self, img, use_nearest=False):
        if use_nearest:
            inter_img = resize_inter_nearest(img, *self._resize_args, **self._resize_kwargs)
        else:
            inter_img = cv2.resize(img, *self._resize_args, **self._resize_kwargs).astype(img.dtype)
        res_img = np.zeros(self._get_res_image_shape(inter_img), img.dtype)
        res_img[
            self._top : self._top + inter_img.shape[0], self._left : self._left + inter_img.shape[1]
        ] = inter_img
        return res_img

    def transform_coords(self, x):
        x[:, 0] = x[:, 0] * self._scale_x + self._left
        x[:, 1] = x[:, 1] * self._scale_y + self._top

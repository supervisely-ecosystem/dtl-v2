# coding: utf-8
# @TODO: drop from public lib? internal instrument

import os
import time

from threading import Lock
from supervisely.sly_logger import logger
from supervisely.io.json import dump_json_file


class TinyTimer:
    def __init__(self):
        self.t = time.time()

    def get_sec(self):  # since creation
        now_t = time.time()
        return now_t - self.t


class StatTimer:
    def __init__(self, logging_interval):
        self.logging_interval = logging_interval
        self.lock = Lock()
        self._q_dct = {}

    def add_value(self, layer_info: dict, val_sec: float):
        if self.logging_interval < 1:
            return  # disabled StatTimer

        object_id = layer_info["id"]

        self.lock.acquire()

        if object_id not in self._q_dct:
            self._q_dct[object_id] = []
        self._q_dct[object_id].append({**layer_info, "val_sec": val_sec})
        logger.debug(
            f"Action '{layer_info['action_name']}' processing time: {val_sec:.6f} sec for {layer_info['items_count']} items"
        )

        # if len(curr_list) >= self.logging_interval:
        # msec_per_one = sum(curr_list) / float(len(curr_list)) * 1000.0
        # logger.trace("StatTimer {}".format(object_id), extra={"msec": msec_per_one})
        # curr_list[:] = []  # clear

        self.lock.release()

    def dump(self):
        dump_json_file(self._q_dct, "stat_timer.json")
        self._q_dct = {}


global_timer = StatTimer(int(os.getenv("STAT_TIMER_LOG_EVERY_RECORDS", "20")))

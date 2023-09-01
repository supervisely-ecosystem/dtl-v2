# coding: utf-8

import os
from supervisely.sly_logger import logger, EventType


def main_wrapper(main_name, main_func, *args, **kwargs):
    try:
        logger.debug('Main started.', extra={'main_name': main_name})
        main_func(*args, **kwargs)
    except Exception as e:
        logger.critical('Unexpected exception in main.', exc_info=True, extra={
            'main_name': main_name,
            'event_type': EventType.TASK_CRASHED,
            'exc_str': str(e),
        })
        logger.debug('Main finished: BAD.', extra={'main_name': main_name})
        os._exit(1)
    else:
        logger.debug('Main finished: OK.', extra={'main_name': main_name})

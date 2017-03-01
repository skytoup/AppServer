# -*- coding: utf-8 -*-
# Created by apple on 2017/1/30.

import logging
from logging.handlers import RotatingFileHandler
from .config import Config

log = logging.getLogger(Config.log_name)

log.setLevel(Config.log_level)


def __init_log():
    log_format = '[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] %(message)s'
    formatter = logging.Formatter(log_format)

    if Config.debug:
        stream_handle = logging.StreamHandler()
        stream_handle.setFormatter(formatter)
        log.addHandler(stream_handle)

    rotating_file_handler = RotatingFileHandler(Config.log_file, maxBytes=Config.log_file_max_byte,
                                                backupCount=Config.log_file_backup_count)
    rotating_file_handler.setFormatter(formatter)
    log.addHandler(rotating_file_handler)


__init_log()

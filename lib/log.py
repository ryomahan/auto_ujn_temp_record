# _*_coding:utf-8_*_
# log 模块

import os
import setting
import logging.config

log_path = getattr(setting, "LOG_PATH", None)
logging_config = getattr(setting, "LOGGING", None)


def log_init():
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    for item in logging_config['handlers']:
        filename = logging_config['handlers'][item]['filename']
        if not os.path.exists(filename):
            f = open(filename, 'w')
            f.close()
    logging.config.dictConfig(logging_config)


def get_logger(name):
    return logging.getLogger(name)

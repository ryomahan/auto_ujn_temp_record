# _*_coding:utf-8_*_
# 配置文件

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.join(BASE_DIR, "log")
DES_JS_PATH = os.path.join(BASE_DIR, "lib", "des", "des.js")

CONFIG = {
    "username": "",
    "password": ""
}

LOGGING = {
    "version": 1,
    "loggers": {
        "access": {
            "level": "INFO",
            "handlers": ["access"]
        },
        "error": {
            "level": "ERROR",
            "propagate": False,
            "handlers": ["error"]
        }
    },
    "handlers": {
        "error": {
            "level": "ERROR",
            "backupCount": 10,
            "encoding": "utf-8",
            "formatter": "general",
            "maxBytes": 1024 * 1024 * 1,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log", "error.log"),
        },
        "access": {
            "level": "INFO",
            "backupCount": 10,
            "encoding": "utf-8",
            "formatter": "general",
            "maxBytes": 1024 * 1024 * 1,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log", "access.log"),
        }
    },
    "formatters": {
        "general": {
            "style": "$",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "$asctime $levelname [$process-$threadName-$thread] "
                      "[$filename-$funcName-$lineno]: $message"
        }
    },
    "disable_existing_loggers": False
}

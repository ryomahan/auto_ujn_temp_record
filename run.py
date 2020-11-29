# -*- coding: utf-8 -*-
# ujn fanxiao website temperature record script
# author: ryoma(ryomahan1996@gmail.com)
# website: blanc.site
import sys
import requests

import setting
from lib.log import log_init
from lib.log import get_logger
from lib.request import get_sso
from lib.request import post_sso
from lib.request import post_fanxiao_sid
from lib.request import post_fanxiao_temperature_record


def init():
    log_init()
    s = requests.Session()
    config = getattr(setting, "CONFIG", None)
    if not(config["username"] and config["password"]):
        logger = get_logger("error")
        message = {
            "action": "从配置文件中获取 username 和 password",
            "status": "失败",
        }
        logger.error(msg=message)
        sys.exit(0)
        
    return s, config["username"], config["password"]


if __name__ == "__main__":
    s, username, password = init()
    cookies, lt, execution = get_sso(s)
    fanxiao_token_url = post_sso(s, cookies, username, password, lt, execution)
    sid = post_fanxiao_sid(s, fanxiao_token_url)
    post_fanxiao_temperature_record(sid)

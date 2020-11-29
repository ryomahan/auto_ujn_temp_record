# -*- coding: utf-8 -*-
# DES 算法处理脚本
import sys

import execjs

import setting
from lib.log import get_logger

des_js_path = getattr(setting, "DES_JS_PATH")


def make_sso_rsa(username, password, lt):
    try:
        f = open(des_js_path, "r", encoding="utf-8")
        line = f.readline()
        js_str = ""
        while line:
            js_str = js_str + line
            line = f.readline()
        ctx = execjs.compile(js_str)
        rsa = (ctx.call("strEnc", f"{username}{password}{lt}", "1", "2", "3"))
        return rsa
    except Exception as e:
        logger = get_logger("error")
        message = {
            "action": "生成 SSO 站点登录所需要的 rsa 变量",
            "status": "失败",
            "message": e
        }
        logger.error(msg=message)
        sys.exit(0)

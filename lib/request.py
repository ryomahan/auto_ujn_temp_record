# _*_coding:utf-8_*_
# 请求模块
import re
import sys
import time
import requests

from lib.des.handler import make_sso_rsa
from lib.log import get_logger


def get_sso(s):
    try:
        headers = {
            "Host": "sso.ujn.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://fanxiao.ujn.edu.cn/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        url = "http://sso.ujn.edu.cn/tpass/login?service=http%3A%2F%2Ffanxiao.ujn.edu.cn%2Fcas%2Findex"
        
        s.headers.clear()
        result = s.get(url=url, headers=headers)
        
        cookies = result.cookies
        html = result.text
        lt_finder = re.search(r"id=\"lt\" name=\"lt\" value=\"(.*)\"", html).groups()
        execution_finder = re.search(r"name=\"execution\" value=\"(.*)\"", html).groups()
        
        if len(lt_finder) > 0:
            lt = lt_finder[0]
        else:
            lt = None

        if len(execution_finder) > 0:
            execution = execution_finder[0]
        else:
            execution = None
        
        return cookies, lt, execution
    except Exception as e:
        logger = get_logger("error")
        message = {
            "action": "GET 请求 SSO 站点登录页，生成构造登录请求所需的关键变量",
            "status": "失败",
            "message": e
        }
        logger.error(msg=message)
        sys.exit(0)


def post_sso(s, cookies, username, password, lt, execution):
    try:
        ul = len(username)
        pl = len(password)
        rsa = make_sso_rsa(username, password, lt)
        url = "http://sso.ujn.edu.cn/tpass/login?service=http%3A%2F%2Ffanxiao.ujn.edu.cn%2Fcas%2Findex"
        headers = {
            "Host":	"sso.ujn.edu.cn",
            "Content-Length": "401",
            "Cache-Control": "max-age=0",
            "Origin": "http://sso.ujn.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://sso.ujn.edu.cn/tpass/login?service=http%3A%2F%2Ffanxiao.ujn.edu.cn%2Fcas%2Findex",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
        }
        data = {
            "rsa": rsa,
            "ul": ul,
            "pl": pl,
            "lt": lt,
            "execution": execution,
            "_eventId": "submit"
        }

        s.headers.clear()
        result = s.post(url=url, headers=headers, cookies=cookies, data=data)

        fanxiao_token_url = result.request.url

        return fanxiao_token_url
    except Exception as e:
        logger = get_logger("error")
        message = {
            "action": "POST 请求 SSO 站点登录页，获取待认证参数的 fanxiao 站点登录 url",
            "status": "失败",
            "message": e
        }
        logger.error(msg=message)
        sys.exit(0)


def post_fanxiao_sid(s, url):
    try:
        headers = {
            "Host": "fanxiao.ujn.edu.cn",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "http://sso.ujn.edu.cn/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language":	"zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }

        s.headers.clear()
        result = s.get(url=url, headers=headers)

        sid = result.request._cookies["sid"]

        return sid
    except Exception as e:
        logger = get_logger("error")
        message = {
            "action": "通过待认证参数的 fanxiao 站点登录 URL 获取 sid",
            "status": "失败",
            "message": e
        }
        logger.error(msg=message)
        sys.exit(0)


def post_fanxiao_temperature_record(sid):
    today_date = time.strftime("%Y-%m-%d", time.localtime())
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    url = "http://fanxiao.ujn.edu.cn/temperatureRecord/createTemperatureRecordCopy"
    headers = {
        "Host": "fanxiao.ujn.edu.cn",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "http://fanxiao.ujn.edu.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.18(0x1700122e) NetType/WIFI Language/zh_CN",
        "Cookie": f"sid={sid}",
        "Content-Length": "104",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive"
    }
    data = {
        "reportTime": today_date,
        "isOut": "2",
        "address": None,
        "travelMode": None,
        "temperatureAm": "36.5",
        "temperaturePm": "36.5",
        "reserveOne": "36.5"
    }

    try:
        result = requests.post(url=url, headers=headers, data=data).json()
        status = result.get("status", 0)
        message = result.get("msg", "未知错误发生")
        if status == 1:
            logger = get_logger("access")
            message = {
                "action": "通过 fanxiao 站点 API 写入温度记录",
                "status": "成功",
                "message": message
            }
            logger.info(msg=message)
            sys.exit(0)
        else:
            logger = get_logger("error")
            message = {
                "action": "通过 fanxiao 站点 API 写入温度记录",
                "status": "失败",
                "message": message
            }
            logger.error(msg=message)
            sys.exit(0)
    except Exception as e:
        logger = get_logger("error")
        message = {
            "action": "构造 fanxiao 站点写入温度记录的 API 请求",
            "status": "失败",
            "message": e
        }
        logger.error(msg=message)
        sys.exit(0)

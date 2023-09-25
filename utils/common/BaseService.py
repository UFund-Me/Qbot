'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-10 00:45:44
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-09-19 23:00:07
FilePath: /Qbot/utils/common/BaseService.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''
# -*-coding=utf-8-*-

import datetime
import json
import os
import re
import time

import parsel
import requests
# from configure.util import send_message_via_wechat
from loguru import logger


class BaseService(object):
    def __init__(self, logfile="default.log"):
        self.logger = logger
        self.logger.add(logfile)
        self.init_const_data()
        self.params = None
        self.cookies = None

    def init_const_data(self):
        """
        常见的数据初始化
        """
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")

    def check_path(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                self.logger.error(e)

    def get_url_filename(self, url):
        return url.split("/")[-1]

    def save_iamge(self, content, path):
        with open(path, "wb") as fp:
            fp.write(content)

    def get(self, url, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.get(
                    url=url,
                    params=self.params,
                    headers=self.headers,
                    cookies=self.cookies,
                )

            except Exception as e:
                self.logger.error("base class error ".format(e))
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    r.encoding = "utf8"
                    result = r.text
                return result

        return None

    def post(self, url, post_data, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.post(url=url, headers=self.headers, data=post_data)

            except Exception as e:
                print(e)
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    result = r.text
                return result

        return None

    @property
    def headers(self):
        raise NotImplementedError

    def parse(self, content):
        """
        页面解析
        """
        response = parsel.Selector(text=content)

        return response

    def process(self, data, history=False):
        """
        数据存储
        """
        pass

    def time_str(self, x):
        return x.strftime("%Y-%m-%d")

    def trading_time(self):
        """
        判定时候交易时间 0 为交易时间， 1和-1为非交易时间
        :return:
        """
        TRADING = 0
        MORNING_STOP = -1
        AFTERNOON_STOP = 1
        NOON_STOP = -1
        current = datetime.datetime.now()
        year, month, day = current.year, current.month, current.day
        start = datetime.datetime(year, month, day, 9, 23, 0)
        noon_start = datetime.datetime(year, month, day, 12, 58, 0)

        morning_end = datetime.datetime(year, month, day, 11, 31, 0)
        end = datetime.datetime(year, month, day, 15, 2, 5)

        if current > start and current < morning_end:
            return TRADING

        elif current > noon_start and current < end:
            return TRADING

        elif current > end:
            return AFTERNOON_STOP

        elif current < start:
            return MORNING_STOP

        else:
            return NOON_STOP

    def notify(self, title):
        print("send_message_via_wechat")
        # send_message_via_wechat(title)

    def weekday(self, day=datetime.datetime.now().strftime("%Y-%m-%d")):
        """判断星期几"""

        if re.search(f"\d{4}-\d{2}-\d{2}", day):
            fmt = "%Y-%m-%d"
        elif re.search("\d{8}", day):
            fmt = "%Y%m%d"
        else:
            raise ValueError("请输入正确的日期格式")

        current_date = datetime.datetime.strptime(day, fmt)
        year_2000th = datetime.datetime(year=2000, month=1, day=2)
        day_diff = current_date - year_2000th
        return day_diff.days % 7

    def is_weekday(self, day=datetime.datetime.now().strftime("%Y-%m-%d")):
        print(day)
        if self.weekday(day) in [0, 6]:
            return False
        else:
            return True

    def execute(self, cmd, data, conn, logger=None):

        cursor = conn.cursor()

        if not isinstance(data, tuple):
            data = (data,)
        try:
            cursor.execute(cmd, data)
        except Exception as e:
            conn.rollback()
            logger.error("执行数据库错误 {},{}".format(e, cmd))
            ret = None
        else:
            ret = cursor.fetchall()
            conn.commit()

        return ret

    def jsonp2json(self, str_):
        return json.loads(str_[str_.find("{") : str_.rfind("}") + 1])

    def set_proxy_param(self, proxy):
        self.proxy_ip = proxy

    def get_proxy(self, retry=10):

        if not hasattr(self, "proxy_ip"):
            raise AttributeError("Please set proxy ip before use it")

        proxyurl = f"http://{self.proxy_ip}/dynamicIp/common/getDynamicIp.do"
        count = 0
        for i in range(retry):
            try:
                r = requests.get(proxyurl, timeout=10)
            except Exception as e:
                print(e)
                count += 1
                print("代理获取失败,重试" + str(count))
                time.sleep(1)

            else:
                js = r.json()
                proxyServer = "://{0}:{1}".format(js.get("ip"), js.get("port"))

                proxies_random = {
                    "http": "http" + proxyServer,
                    "https": "https" + proxyServer,
                }
                return proxies_random

        return None

    def convert_timestamp(self, t):
        return datetime.datetime.fromtimestamp(int(t / 1000)).strftime("%Y-%m-%d")


class HistorySet(object):
    def __init__(self, expire=1800):
        self.data = {}
        self.expire = expire

    def add(self, value):
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(seconds=self.expire)
        try:
            hash(value)
        except:  # noqa E722
            raise ValueError("value not hashble")
        else:
            self.data.update({value: expire})

    def is_expire(self, value):
        # 没有过期 返回 False
        if value not in self.data or self.data[value] < datetime.datetime.now():
            return True
        else:
            return False


if __name__ == "__main__":
    base = BaseService()
    base.is_weekday()
    # base.set_proxy_param()
    print(base.get_proxy())

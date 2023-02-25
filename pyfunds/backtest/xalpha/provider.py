# -*- coding: utf-8 -*-
"""
codebase related to data API provider which require further authetications
"""

import os
import sys
from functools import wraps
from base64 import b64decode, b64encode

try:
    from jqdatasdk import auth

    jq_source = True
except ImportError:
    jq_source = False

from xalpha.exceptions import DataSourceNotFound


thismodule = sys.modules[__name__]

providers_list = ["jq"]


b64encode_s = lambda s: b64encode(s.encode("utf-8")).decode("utf-8")
b64decode_s = lambda s: b64decode(s.encode("utf-8")).decode("utf-8")
# 注意 base64 毫无加密功能，因此请自己考虑将密码本地化后的便捷性与安全性的平衡


def set_proxy(proxy=None):
    """
    设置代理，部分数据源可能国内网络环境不稳定。比如标普指数官网。
    还有一些数据源很快就会封 IP，需要设置代理，比如人民币中间价官网，建议直接把中间价数据缓存到本地，防止反复爬取。

    :param proxy: str. format as "http://user:passwd@host:port" user passwd part can be omitted if not set. None 代表取消代理
    :return:
    """
    if proxy:
        os.environ["http_proxy"] = proxy
        os.environ["https_proxy"] = proxy
        setattr(thismodule, "proxy", proxy)
    else:
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""
        setattr(thismodule, "proxy", None)


def set_jq_data(user=None, pswd=None, persistent=False, debug=False):
    """
    设置聚宽数据源，需申请聚宽的 jqdata 试用权限。

    :param user: str。聚宽用户注册手机号。
    :param pswd: str。聚宽用户密码。
    :param persistent: Optional[bool]. Default False. 如果是 True，则意味着聚宽用户名和密码将进行本地存储，
            以后再使用 xalpha 则无须在输入密码调用该函数。请注意，如果这样做，你的聚宽账户和密码将保存在你的本地电脑，
            仅有简单编码，无加密保护。请谨慎权衡本地保存的使用便利性和聚宽账户的安全性。
            （如果你能保证使用 xalpha 的电脑不被黑，那么就没啥其他安全问题）
    :param debug: Optional[bool]. Default False, if True, 那么不去真实验证聚宽数据源，而直接视为注册，用于测试或者直接在聚宽研究环境运行时。
    :return:
    """
    if debug:
        setattr(thismodule, "jq_auth", True)
        # do nothing for real
        return True
    if not jq_source:
        print("You have not installed jqdatasdk package")
        return False
    xadir = os.path.dirname(os.path.abspath(__file__))
    authpath = os.path.join(xadir, "jq_auth.txt")

    if not user or not pswd:
        if os.path.exists(authpath):
            with open(authpath, "r") as f:
                user, pswd = f.readlines()
                user = b64decode_s(user.strip())
                pswd = b64decode_s(pswd.strip())
        else:
            setattr(thismodule, "jq_auth", False)
            return False

    auth(user, pswd)
    setattr(thismodule, "jq_auth", True)
    if persistent:
        user = b64encode_s(user)
        pswd = b64encode_s(pswd)
        with open(authpath, "w") as f:
            f.writelines([user + "\n" + pswd])
    return True


def data_source(s):
    """
    用以强制要求某些数据源已注册的装饰器。

    :param s: 数据源，现在仅支持 "jq"
    :return:
    """

    def protected(f):
        @wraps(f)
        def wrapper(*args, **kws):
            if getattr(thismodule, s + "_auth", False):
                return f(*args, **kws)
            else:
                raise DataSourceNotFound("Data source %s is not authenticated" % s)

        return wrapper

    return protected


def show_providers():
    """
    展示所有已注册的数据源。

    :return:
    """
    l = []
    for source in providers_list:
        if getattr(thismodule, source + "_auth", False):
            l.append(source)
    return l


def initialization():
    set_proxy()
    for source in providers_list:
        if getattr(thismodule, source + "_source", False):
            getattr(thismodule, "set_" + source + "_data")()


initialization()

# TODO: some utilities for merging datas, say dwonload some partial data archive from the web and merge it to my own data dir

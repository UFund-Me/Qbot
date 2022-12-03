# -*- coding: utf-8 -*-
import logging
import sys

from easytrader.log import logger
from easytrader.mock_trader import MockTrader
from easytrader.eastmoney_trader import EastMoneyTrader

if sys.version_info <= (3, 5):
    raise TypeError("不支持 Python3.5 及以下版本，请升级")

def use(broker, debug=False, **kwargs):
    """用于生成特定的券商对象
    :param broker:券商名支持 ['yh_client', '银河客户端'] ['ht_client', '华泰客户端']
    :param debug: 控制 debug 日志的显示, 默认为 True
    :param initial_assets: [雪球参数] 控制雪球初始资金，默认为一百万
    :return the class of trader

    Usage::

        >>> import easytrader
        >>> user = easytrader.use('xq')
        >>> user.prepare('xq.json')
    """
    if debug:
        logger.setLevel(logging.DEBUG)

    if broker.lower() in ["mock"]:
        return MockTrader(**kwargs)

    if broker.lower() in ["eastmoney", "东财", "东方财富"]:
        return EastMoneyTrader(**kwargs)

    raise NotImplementedError


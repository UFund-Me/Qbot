#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************

import easyquant
from easyquant import DefaultLogHandler

print("测试 DEMO")

# 东财
broker = "eastmoney"

# 自己准备
# {
#     "user": "",
#     "password": ""# }
need_data = "account.json"

log_type = "file"

log_handler = DefaultLogHandler(name="测试", log_type=log_type, filepath="logs.log")

m = easyquant.MainEngine(
    broker,
    need_data,
    quotation="online",
    # 1分钟K线
    bar_type="1m",
    log_handler=log_handler,
)
m.is_watch_strategy = True  # 策略文件出现改动时,自动重载,不建议在生产环境下使用
m.load_strategy()
m.start()

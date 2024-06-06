"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-02-13 23:24:17
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-10 00:00:16
FilePath: /Qbot/pytrader/doc/11.eastmoney_with_prom_grafana/fetch_stock.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
"""

import time

import requests
from prometheus_client import CollectorRegistry, Gauge, start_http_server

reg = CollectorRegistry()
gauge = Gauge("rank", "人气榜排名", ["stock_id"], registry=reg)


def process_request():
    url = "https://emappdata.eastmoney.com/stockrank/getAllCurrentList"
    kwargs = {
        "appId": "appId01",
        "pageNo": 1,
        "pageSize": "100",
    }
    result = requests.post(url, json=kwargs).json()
    for i in result.get("data", []):
        gauge.labels(stock_id=i["sc"]).set(i["rk"])
    time.sleep(60)


if __name__ == "__main__":
    start_http_server(8000, registry=reg)
    while True:
        process_request()

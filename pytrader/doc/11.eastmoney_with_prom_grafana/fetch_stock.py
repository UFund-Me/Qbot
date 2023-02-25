# Python实用宝典
# 2021-06-13
# 文件名: fetch_stock.py
import time
import requests
from prometheus_client import start_http_server, CollectorRegistry, Gauge


reg = CollectorRegistry()
gauge = Gauge(
    'rank', '人气榜排名',
    ['stock_id'], registry=reg
)


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


if __name__ == '__main__':
    start_http_server(8000, registry=reg)
    while True:
        process_request()

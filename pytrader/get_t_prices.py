import datetime
from typing import List

from easyquant.quotation import use_quotation


def get_t_price(code: str):
    df = quotation.get_bars(code, count=1, end_dt=datetime.datetime.now() - datetime.timedelta(days=1))

    last = df[-1:]

    high = last.high[0]
    low = last.low[0]
    close = last.close[0]
    pivot = (high + low + close) / 3

    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    s1 = 2 * pivot - high
    s2 = pivot - (high - low)

    return r1, r2, s1, s2


def get_t_prices(codes: List[str]):
    return [get_t_price(code) for code in codes]


quotation = use_quotation('jqdata')
codes = {
    # "512580": "碳中和",
    # "002233": "塔牌",
    # "002415": "海康",
    # "600104": "上汽",
    "002230": "讯飞",
    # "600036": "招行",
    "601318": "平安",
    # "300750": "宁德时代",
    # "159949": "创业板50",
    # "600900": "长电",
    "600048": "保利"}

for stock in codes.keys():
    r1, r2, s1, s2 = get_t_price(stock)

    print("%s %s : 阻力价格1 = %s, 阻力价格2 = %s, 支撑1 =%s , 支撑2 =%s" % (codes[stock], stock, r1, r2, s1, s2))



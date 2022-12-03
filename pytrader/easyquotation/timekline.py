# coding:utf8
"""
# pylint: disable=line-too-long
url = "http://data.gtimg.cn/flashdata/hushen/minute/sz000001.js?maxage=110&0.28163905744440854"
"""

import re
from . import basequotation, helpers


class TimeKline(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    max_num = 1

    @property
    def stock_api(self) -> str:
        return "http://data.gtimg.cn/flashdata/hushen/minute/"

    def _gen_stock_prefix(self, stock_codes):
        return [
            helpers.get_stock_type(code) + code[-6:] + ".js"
            for code in stock_codes
        ]

    def _fetch_stock_data(self, stock_list):
        """因为 timekline 的返回没有带对应的股票代码，所以要手动带上"""
        res = super()._fetch_stock_data(stock_list)

        with_stock = []
        for stock, resp in zip(stock_list, res):
            if resp is not None:
                with_stock.append((stock, resp))
        return with_stock

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = dict()
        for stock_code, stock_detail in rep_data:
            # pylint: disable=line-too-long
            # res like ['min_data="', 'date:180413', '0930 11.64 29727', '0931 11.65 52410']
            res = re.split(r"\\n\\\n", stock_detail)
            date = "20{}".format(res[1][-6:])
            time_data = list(
                d.split() for d in res[2:] if re.match(r"\d{4}", d)
            )
            stock_dict[stock_code[:-3]] = {"date": date, "time_data": time_data}
        return stock_dict

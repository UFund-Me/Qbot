# coding:utf8
"""
# pylint: disable=line-too-long
url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh688017_5_1632742847429=/CN_MarketDataService.getKLineData?symbol=sh688017&scale=5&ma=no&datalen=1023"
"""

import re
import json
from . import basequotation, helpers


class SinaTimeKline(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    max_num = 1

    @property
    def stock_api(self) -> str:
        return "https://quotes.sina.cn/cn/api/jsonp_v2.php/jsonp/CN_MarketDataService.getKLineData?symbol="

    def _gen_stock_prefix(self, stock_codes):
        return [
            helpers.get_stock_type(code) + code[-6:] + "&scale=5&ma=no&datalen=1023"
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
            start = stock_detail.index('jsopnp(') + len('jsopnp(')
            # pylint: disable=line-too-long
            stock_detail = stock_detail[start:-1]
            stock_dict[stock_code] = json.loads(stock_detail)
        return stock_dict

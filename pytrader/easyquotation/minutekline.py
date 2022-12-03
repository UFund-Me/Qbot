# coding:utf8
"""
# pylint: disable=line-too-long
url = "https://ifzq.gtimg.cn/appstock/app/kline/mkline?param=sz002230,m30,,320&_var=m30_today&r=0.42616245339179404"
"""

import re
import json
from . import basequotation, helpers


class MinuteTimeKline(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    max_num = 80
    minute = 5

    @property
    def stock_api(self) -> str:
        return "https://ifzq.gtimg.cn/appstock/app/kline/mkline?param="

    def real(self, stock_codes, prefix=False, **kwargs):
        if "max_num" in kwargs:
            self.max_num = kwargs["max_num"]

        if "minute" in kwargs:
            self.minute = kwargs["minute"]

        return super().real(stock_codes, prefix=prefix, **kwargs)

    def _gen_stock_prefix(self, stock_codes):
        return [
            '%s%s,m%d,,%d&_var=m%d_today&r=0.42616245339179404' %
            (helpers.get_stock_type(code), code[-6:], self.minute, self.max_num, self.minute)
            for code in stock_codes
        ]

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = dict()
        _var = 'm%d_today=' % self.minute
        prefix = kwargs["prefix"] if kwargs["prefix"] in kwargs else False
        for stock_detail in rep_data:
            # pylint: disable=line-too-long
            # res like ['min_data="', 'date:180413', '0930 11.64 29727', '0931 11.65 52410']
            stock_detail = stock_detail.replace(_var, '')
            result = json.loads(stock_detail)['data']
            for code in result:
                stock_dict[code if prefix else code[2:]] = result[code]['m%d' % self.minute]
        return stock_dict

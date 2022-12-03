# coding:utf8
"""
# pylint: disable=line-too-long
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00001,day,,,660,qfq&r=0.7773272375526847"

url 参数改动
股票代码 :hk00001
日k线天数：660

更改为需要获取的股票代码和天数例如：

# pylint: disable=line-too-long
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847"

"""
import json
import re

from . import basequotation


class DayKline(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    max_num = 1

    @property
    def stock_api(self) -> str:
        # pylint: disable=line-too-long
        return "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param="

    def _gen_stock_prefix(self, stock_codes, day=1500):
        return ["hk{},day,,,{},qfq".format(code, day) for code in stock_codes]

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = {}
        for raw_quotation in rep_data:
            raw_stocks_detail = re.search(r"=(.*)", raw_quotation).group(1)
            stock_details = json.loads(raw_stocks_detail)
            for stock, value in stock_details["data"].items():
                stock_code = stock[2:]
                if "qfqday" in value:
                    stock_detail = value["qfqday"]
                else:
                    stock_detail = value.get("day")
                if stock_detail is None:
                    print("stock code data not find %s"%stock_code)
                    continue
                stock_dict[stock_code] = stock_detail
                break

        return stock_dict


if __name__ == "__main__":
    pass

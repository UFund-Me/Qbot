import abc
import datetime
import json
import os

import jqdatasdk
import pandas
import pandas as pd
import tushare as ts
from easyquant.easydealutils.time import get_all_trade_days
from easyquant.models import SecurityInfo
from easyquotation.bar import get_price
from easytrader.utils.misc import file2dict
from jqdatasdk import finance, query
from pandas import DataFrame


class Quotation(metaclass=abc.ABCMeta):
    """行情获取基类"""

    def get_bars(
        self,
        security,
        count,
        unit="1d",
        fields=["date", "open", "high", "low", "close", "volume"],
        include_now=False,
        end_dt=None,
    ) -> DataFrame:
        """
        获取历史数据(包含快照数据), 可查询单个标的多个数据字段

        :param security 股票代码
        :param count 大于0的整数，表示获取bar的个数。如果行情数据的bar不足count个，返回的长度则小于count个数。
        :param unit bar的时间单位, 支持如下周期：'1m', '5m', '15m', '30m', '60m', '120m', '1d', '1w', '1M'。'1w' 表示一周，‘1M' 表示一月。
        :param fields 获取数据的字段， 支持如下值：'date', 'open', 'close', 'high', 'low', 'volume', 'money'
        :param include_now 取值True 或者False。 表示是否包含当前bar, 比如策略时间是9:33，unit参数为5m， 如果 include_now=True,则返回9:30-9:33这个分钟 bar。
        :param end_dt: 查询的截止时间
        :param fq_ref_date: 复权基准日期，为None时为不复权数据
        :param df: 默认为True，传入单个标的返回的是一个dataframe，传入多个标的返回的是一个multi-index dataframe
                当df=False的时候，当单个标的的时候，返回一个np.ndarray，多个标的返回一个字典，key是code，value是np.array；
        :return numpy.ndarray格式
        """
        pass

    def get_all_trade_days(self):
        """
        所有交易日期
        :return:
        """
        # trade_days = jqdatasdk.get_all_trade_days()
        # data = pd.Series(trade_days.tolist())
        # data = data.apply(lambda x: x.strftime("%Y-%m-%d"))
        # return data.values.tolist()
        return get_all_trade_days()

    def get_price(self, security: str, date) -> float:
        df = self.get_bars(security, 1, unit="1d", end_dt=date)
        return df.close[-1]

    def get_north_money(self, date):
        return 0

    def get_stock_info(self, security: str) -> SecurityInfo:
        security = SecurityInfo()
        security.code = security
        security.name = security
        return SecurityInfo


def is_shanghai(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, "stock code need str type"
    sh_head = ("50", "51", "60", "90", "110", "113", "132", "204", "5", "6", "9", "7")
    return stock_code.startswith(sh_head)


def to_date_str(dt):
    if dt is None:
        return None
    if isinstance(dt, datetime.date) or isinstance(dt, datetime.datetime):
        return dt.strftime("%Y-%m-%d")


class TushareQuotation(Quotation):
    """
    tushare 行情
    """ ""

    def __init__(self):
        tushare_config = file2dict("tushare.json")
        ts.set_token(tushare_config["token"])

    def get_stock_type(self, stock_code: str):
        return "SH" if is_shanghai(stock_code) else "SZ"

    def _format_code(self, code: str) -> str:
        return "%s.%s" % (code, self.get_stock_type(code))

    def _get_cache_key(self, security, end_dt, unit):
        return "data/tushare_%s_%s_%s.csv" % (
            self._format_code(security),
            to_date_str(end_dt),
            unit,
        )

    def get_bars(
        self,
        security,
        count,
        unit="1d",
        fields=["trade_date", "open", "high", "low", "close"],
        include_now=False,
        end_dt=None,
    ) -> DataFrame:

        if unit == "1d":
            unit = "D"

        cache_file = self._get_cache_key(security, end_dt, unit)

        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file)
            df.index = pandas.to_datetime(df["trade_date"])
            return df

        df = ts.pro_bar(
            ts_code=self._format_code(security),
            end_date=to_date_str(end_dt),
            freq=unit,  # 只免费
            asset="E",
            limit=count,
        )
        df.index = pandas.to_datetime(df["trade_date"])
        df.sort_index(inplace=True)

        df.to_csv(cache_file)

        return df


class JQDataQuotation(Quotation):
    """
    JQData行情
    """ ""

    cache = {}

    def __init__(self):
        jqdata = {"user": os.getenv("USER_ID"), "password": os.getenv("PASSWORD")}
        with open("jqdata.json", "w", encoding="utf-8") as fw:
            json.dump(jqdata, fw, indent=4, ensure_ascii=False)

        config = file2dict("jqdata.json")
        print("user:  ", config["user"])
        print("password:  ", config["password"])

        jqdatasdk.auth(config["user"], config["password"])

    def _get_cache_key(self, security, end_dt, unit):
        return "%s_%s_%s" % (self._format_code(security), to_date_str(end_dt), unit)

    def get_stock_type(self, stock_code: str):
        return ".XSHG" if is_shanghai(stock_code) else ".XSHE"

    def _format_code(self, code: str) -> str:
        return "%s%s" % (code, self.get_stock_type(code))

    def get_north_money(self, date):
        n_sh = finance.run_query(
            query(finance.STK_ML_QUOTA)
            .filter(
                finance.STK_ML_QUOTA.day <= date, finance.STK_ML_QUOTA.link_id == 310001
            )
            .order_by(finance.STK_ML_QUOTA.day.desc())
            .limit(10)
        )
        n_sz = finance.run_query(
            query(finance.STK_ML_QUOTA)
            .filter(
                finance.STK_ML_QUOTA.day <= date, finance.STK_ML_QUOTA.link_id == 310002
            )
            .order_by(finance.STK_ML_QUOTA.day.desc())
            .limit(10)
        )
        total_net_in = 0
        for i in range(0, 3):
            sh_in = n_sh["buy_amount"][i] - n_sh["sell_amount"][i]
            sz_in = n_sz["buy_amount"][i] - n_sz["sell_amount"][i]
            amount = sh_in + sz_in
            total_net_in += amount
        return total_net_in

    def get_bars(
        self,
        security,
        count,
        unit="1d",
        fields=["date", "open", "high", "low", "close", "volume"],
        include_now=True,
        end_dt=None,
    ) -> DataFrame:

        query_dt = end_dt
        if not isinstance(query_dt, datetime.datetime):
            query_dt = datetime.datetime.strptime(query_dt, "%Y-%m-%d")

        query_dt += datetime.timedelta(days=1)

        if "date" not in fields:
            fields.append("date")

        cache_key = self._get_cache_key(security, query_dt, unit)

        if cache_key in self.cache:
            df = self.cache[cache_key]
            return df[df.index <= end_dt] if "m" in unit else df

        cache_file = "data/jqdata-%s.csv" % cache_key

        if os.path.exists(cache_file):
            df = pd.read_csv(cache_file)
            df.index = df.date
            self.cache[cache_key] = df
            return df[df.index <= end_dt] if "m" in unit else df

        df = jqdatasdk.get_bars(
            self._format_code(security),
            10000,
            unit=unit,
            fields=fields,
            include_now=include_now,
            # 取整天的数据
            end_dt=to_date_str(query_dt),
            fq_ref_date=datetime.datetime.now(),
        )
        df.index = df.date
        df.sort_index(inplace=True)
        # 放入缓存
        self.cache[cache_key] = df

        df.to_csv(cache_file)

        # 过滤数据
        return df[df.index <= end_dt] if "m" in unit else df

    def get_stock_info(self, security: str):
        return jqdatasdk.get_security_info(self._format_code(security))


class FreeOnlineQuotation(Quotation):
    """
    实时行情
    """ ""

    def get_stock_type(self, stock_code: str):
        return "sh" if is_shanghai(stock_code) else "sz"

    def _format_code(self, code: str) -> str:
        return "%s%s" % (self.get_stock_type(code), code)

    def get_bars(
        self,
        security,
        count,
        unit="1d",
        fields=["date", "open", "high", "low", "close", "volume"],
        include_now=False,
        end_dt=None,
    ) -> DataFrame:
        df = get_price(
            self._format_code(security), end_date=end_dt, count=security, frequency=unit
        )
        return df


def use_quotation(source: str) -> Quotation:
    """
    对外API，行情工厂
    :param source:
    :return:
    """
    if source in ["jqdata"]:
        return JQDataQuotation()
    if source in ["tushare"]:
        return TushareQuotation()
    return FreeOnlineQuotation()


if __name__ == "__main__":
    qutation = use_quotation("jqdata")
    # df1 = qutation.get_bars("002230", 200, unit="5m", end_dt=datetime.datetime.now())
    # df2 = qutation.get_bars("002230", 200, unit="5m", end_dt=datetime.datetime.now())
    # print(df1)
    # print(df2)
    print(qutation.get_price("002230", datetime.datetime.now()))

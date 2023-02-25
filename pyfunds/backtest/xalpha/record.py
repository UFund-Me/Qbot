# -*- coding: utf-8 -*-
"""
module for status table IO
"""
import pandas as pd

from xalpha.cons import convert_date, yesterdayobj


class record:
    """
    basic class for status table read in from csv file.
    staus table 是关于对应基金的申赎寄账单，不同的行代表不同日期，不同的列代表不同基金，
    第一行各单元格分别为 date, 及基金代码。第一列各单元格分别为 date 及各个交易日期，形式 eg. 20170129
    表格内容中无交易可以直接为空或0，申购为正数，对应申购金额（申购费扣费前状态），赎回为负数，对应赎回份额，
    注意两者不同，恰好对应基金的金额申购份额赎回原则，记录精度均只完美支持一位小数。
    几个更具体的特殊标记：

    1. 小数点后第二位如果是5，且当日恰好为对应基金分红日，标志着选择了分红再投入的方式，否则默认分红拿现金。（该默认行为可反转）

    2. 对于赎回的负数，如果是一个绝对值小于 0.005 的数，标记了赎回的份额占当时总份额的比例而非赎回的份额数目，
    其中0.005对应全部赎回，线性类推。eg. 0.001对应赎回20%。

    3. 账单上自定义申购费和赎回费，小数点后第三位的 5 标记，代表了该数据费用是自定义的。注意这和 -0.005 代表全部卖出并不冲突，其原因是自定义费用，
    前边肯定不全为 0。第三位 5 之后，代表了 1% 位。也即 -51.28515 意义是赎回 51.28 份，赎回费为 1.5%. 200.205 代表申购 200.2 元，申购费为0
    （因为标记位 5 后没有其他非零数字）。这种自定义通常可用于定期支付型基金的强制卖出（不收赎回费）和基金公司官网申购基金时申购费全免的记录。

    关于基金行为的设定，基金份额是四舍五入0 还是全部舍弃 1， 基金是默认现金分红 0 还是分红再投 2， 基金是赎回数目对应份额 0 还是金额 4 （只支持货币基金），
    将三个选项加起来得到 0-7 的数字，代表了基金的交易性质，默认全部为0。该性质即可以记录在 matrix 形式记账单紧贴基金代码行头的下一行，同时 record 读取时，
    ``record(path, fund_property=True)`` 设定 fund_property 参数, 或直接在记账单第二行日期栏写上 property 即可。每个基金代码对应一个 0 到 7 的数字。
    也可为空，默认为 0。

    此外如不改变记账单，也可在 :class:`xalpha.multiple.mul` 类初始化时，传入 property=dict, 字典内容为 {"基金代码"：0-7 数字}。默认为0的代码可不添加。

    对于不同格式的记账单的例子，可在 github repo 中 tests 文件夹内的 demo*.csv 参考。

    :param path: string for the csv file path or pd.DataFrame
    :param format: str. Default is "matrix". Can also be "list"。list 形式的账单更类似流水单。总共三列，每行由日期基金号和金额组成。
                三栏标题分别为 date，fund 和 trade。其中日期的形式是 %Y/%m/%d. 该形式与默认的 matrix 不包含 "/" 不同。
    :param fund_property: bool. Default False. If True, 基金号下第一行的数字标记对应基金参数（暂时只支持 matrix 形式账单）。
    :param readkwds: keywords options for pandas.read_csv() function. eg. skiprows=1, skipfooter=2,
        see more on `pandas doc <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html>`_.
    """

    def __init__(
        self, path="input.csv", format="matrix", fund_property=False, **readkwds
    ):
        if isinstance(path, str):
            df = pd.read_csv(path, **readkwds)
        else:  # path itself is a pd.DataFrame
            df = path
        if df.iloc[0]["date"] == "property":
            fund_property = True
        if format == "matrix":
            df.fillna(0, inplace=True)
            df.columns = ["date"] + [
                c.zfill(6) if c.isdigit() else c for c in df.columns[1:]
            ]
            if fund_property:
                self.property = df.iloc[0]
                df2 = df.iloc[1:]
                df2 = df2.sort_values(by="date", ascending=True)
                df2.date = [
                    # pd.Timestamp.strptime(str(int(df.iloc[i].date)), "%Y%m%d")
                    # higher version of pandas timestamp doesn't support strptime anymore? why? what is the gain here?
                    pd.to_datetime(str(int(df2.iloc[i].date)), format="%Y%m%d")
                    for i in range(len(df2))
                ]
                self.status = df2
            else:
                df = df.sort_values(by="date", ascending=True)
                df.date = [
                    pd.to_datetime(str(int(df.iloc[i].date)), format="%Y%m%d")
                    for i in range(len(df))
                ]
                self.status = df

        elif format == "list":
            fund = df.fund.unique()
            # fund_s = ["{:06d}".format(i) for i in fund]
            fund_s = [str(c).zfill(6) if str(c).isdigit() else c for c in fund]
            date_s = df.date.unique()
            dfnew = pd.DataFrame(
                columns=["date"] + fund_s, index=date_s, dtype="float64"
            )
            dfnew.fillna(0, inplace=True)
            dfnew["date"] = [pd.to_datetime(i, format="%Y/%m/%d") for i in date_s]
            for i in range(len(df)):
                dfnew.at[df.iloc[i].date, "{:06d}".format(df.iloc[i].fund)] += df.iloc[
                    i
                ].trade
            dfnew = dfnew.sort_values(by=["date"])
            self.status = dfnew

    def sellout(self, date=yesterdayobj(), ratio=1):
        """
        Sell all the funds in the same ratio on certain day, it is a virtual process,
        so it can happen before the last action exsiting in the cftable, by sell out earlier,
        it means all actions behind vanish. The status table in self.status would be directly changed.

        :param date: string or datetime obj of the selling date
        :param ratio: float between 0 to 1, the ratio of selling for each funds
        """
        date = convert_date(date)
        s = self.status[self.status["date"] <= date]
        row = []
        ratio = ratio * 0.005
        for term in s.columns:
            if term != "date":
                row.append(-ratio)
            else:
                row.append(date)
        s = s.append(pd.DataFrame([row], columns=s.columns), ignore_index=True)
        self.status = s

    def save_csv(self, path=None, index=False, **tocsvkwds):
        """
        save the status table to csv file in path, no returns

        :param path: string of file path
        :param index: boolean, whether save the index to the csv file, default False
        :param tocsvkwds: keywords options for pandas.to_csv() function, see
            `pandas doc <https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_csv.html>`_.
        """
        self.status.to_csv(path, index=index, **tocsvkwds)


class irecord(record):
    """
    场内记账单抽象。对于场内交易，记账单毫无疑问需要记录净值，而无法依赖自动查询（因为净值实时变化）。
    记账单的格式为5列，分别为 date，code，value，share，fee。日期格式为%Y%m%d, 例 20200202。
    代码格式与 :func:`xalpha.universal.get_daily` 要求相同。对于常见的 A 股标的，格式为 SH501018。
    value 列记录买入卖出或场内申购赎回对应的成交净值单价。share 记录实际上份额的增减，正数代表买入。
    fee 栏对应了每笔交易实际的佣金，也可不记录，则默认均为0。记账单不要求严格按时间排序。
    该类处理的记账单可以提供给 :class:`xalpha.trade.itrade` 和 :class:`xalpha.multiple.imul` 使用，进行场内交易的整合分析。
    """

    def __init__(self, path="input.csv", **readkwds):
        if isinstance(path, str):
            df = pd.read_csv(path, **readkwds)
        else:
            df = path
        df.fillna(0, inplace=True)
        df.date = [
            pd.to_datetime(df.iloc[i].date, format="%Y%m%d") for i in range(len(df))
        ]
        if "fee" not in df.columns:
            df = df.assign(fee=[0] * len(df))
        df = df.sort_values(by="date", ascending=True)
        self.status = df

    def filter(self, code, start=None, end=None):
        df = self.status[self.status["code"] == code]
        if start:
            df = df[df["date"] >= start]
        if end:
            df = df[df["date"] <= end]
        return df

    def sellout(self, date=yesterdayobj(), ratio=1):
        raise NotImplementedError()

    def totfee(self):
        """
        累计交给券商的过路费总额

        :return:
        """
        return self.status["fee"].sum()


Record = record
IRecord = irecord

# TODO: merge multiple status or istatus csv into one

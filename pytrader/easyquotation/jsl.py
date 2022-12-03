# coding:utf8
"""
获取集思路的数据
"""
import json
import time

import requests


class Jsl:
    """
    抓取集思路的分级A数据
    """

    # 分级A的接口
    __funda_url = "http://www.jisilu.cn/data/sfnew/funda_list/?___t={ctime:d}"

    # 分级B的接口
    __fundb_url = "http://www.jisilu.cn/data/sfnew/fundb_list/?___t={ctime:d}"

    # 母基接口
    __fundm_url = "https://www.jisilu.cn/data/sfnew/fundm_list/?___t={ctime:d}"

    # 分级套利的接口
    __fundarb_url = (
        "http://www.jisilu.cn/data/sfnew/arbitrage_vip_list/?___t={ctime:d}"
    )

    # 集思录登录接口
    __jsl_login_url = "https://www.jisilu.cn/account/ajax/login_process/"

    # 集思录 ETF 接口
    # pylint: disable=line-too-long
    __etf_index_url = "https://www.jisilu.cn/data/etf/etf_list/?___jsl=LST___t={ctime:d}&rp=25&page=1"

    # 黄金 ETF , 货币 ETF 留坑,未完成
    __etf_gold_url = (
        "https://www.jisilu.cn/jisiludata/etf.php?qtype=pmetf&___t={ctime:d}"
    )
    __etf_money_url = (
        "https://www.jisilu.cn/data/money_fund/list/?___t={ctime:d}"
    )

    # 集思录QDII接口
    __qdii_url = "https://www.jisilu.cn/data/qdii/qdii_list/?___t={ctime:d}"
    # 可转债
    __cb_url = "https://www.jisilu.cn/data/cbnew/cb_list/?___t={ctime:d}"

    # 分级A数据
    # 返回的字典格式
    # { 150022:
    # {'abrate': '5:5',
    #  'calc_info': None,
    #  'coupon_descr': '+3.0%',
    #  'coupon_descr_s': '+3.0%',
    #  'fund_descr': '每年第一个工作日定折，无下折，A不参与上折，净值<1元无定折',
    #  'funda_amount': 178823,
    #  'funda_amount_increase': '0',
    #  'funda_amount_increase_rt': '0.00%',
    #  'funda_base_est_dis_rt': '2.27%',
    #  'funda_base_est_dis_rt_t1': '2.27%',
    #  'funda_base_est_dis_rt_t2': '-0.34%',
    #  'funda_base_est_dis_rt_tip': '',
    #  'funda_base_fund_id': '163109',
    #  'funda_coupon': '5.75',
    #  'funda_coupon_next': '4.75',
    #  'funda_current_price': '0.783',
    #  'funda_discount_rt': '24.75%',
    #  'funda_id': '150022',
    #  'funda_increase_rt': '0.00%',
    #  'funda_index_id': '399001',
    #  'funda_index_increase_rt': '0.00%',
    #  'funda_index_name': '深证成指',
    #  'funda_left_year': '永续',
    #  'funda_lower_recalc_rt': '1.82%',
    #  'funda_name': '深成指A',
    #  'funda_nav_dt': '2015-09-14',
    #  'funda_profit_rt': '7.74%',
    #  'funda_profit_rt_next': '6.424%',
    #  'funda_value': '1.0405',
    #  'funda_volume': '0.00',
    #  'fundb_upper_recalc_rt': '244.35%',
    #  'fundb_upper_recalc_rt_info': '深成指A不参与上折',
    #  'last_time': '09:18:22',
    #  'left_recalc_year': '0.30411',
    #  'lower_recalc_profit_rt': '-',
    #  'next_recalc_dt': '<span style="font-style:italic">2016-01-04</span>',
    #  'owned': 0,
    #  'status_cd': 'N'}
    # }

    def __init__(self):
        self.__funda = None
        self.__fundm = None
        self.__fundb = None
        self.__fundarb = None
        self.__etfindex = None
        self.__qdii = None
        self.__cb = None

    @staticmethod
    def formatfundajson(fundajson):
        """格式化集思录返回的json数据,以字典形式保存"""
        result = {}
        for row in fundajson["rows"]:
            funda_id = row["id"]
            cell = row["cell"]
            result[funda_id] = cell
        return result

    @staticmethod
    def formatfundbjson(fundbjson):
        """格式化集思录返回的json数据,以字典形式保存"""
        result = {}
        for row in fundbjson["rows"]:
            cell = row["cell"]
            fundb_id = cell["fundb_id"]
            result[fundb_id] = cell
        return result

    @staticmethod
    def formatetfindexjson(fundbjson):
        """格式化集思录返回 指数ETF 的json数据,以字典形式保存"""
        result = {}
        for row in fundbjson["rows"]:
            cell = row["cell"]
            fundb_id = cell["fund_id"]
            result[fundb_id] = cell
        return result

    @staticmethod
    def formatjisilujson(data):
        result = {}
        for row in data["rows"]:
            cell = row["cell"]
            id_ = row["id"]
            result[id_] = cell
        return result

    @staticmethod
    def percentage2float(per):
        """
        将字符串的百分数转化为浮点数
        :param per:
        :return:
        """
        return float(per.strip("%")) / 100.

    def funda(
        self,
        fields=None,
        min_volume=0,
        min_discount=0,
        ignore_nodown=False,
        forever=False,
    ):
        """以字典形式返回分级A数据
        :param fields:利率范围，形如['+3.0%', '6.0%']
        :param min_volume:最小交易量，单位万元
        :param min_discount:最小折价率, 单位%
        :param ignore_nodown:是否忽略无下折品种,默认 False
        :param forever: 是否选择永续品种,默认 False
        """
        if fields is None:
            fields = []

        # 添加当前的ctime
        self.__funda_url = self.__funda_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__funda_url)
        # 获取返回的json字符串
        fundajson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatfundajson(fundajson)
        # 过滤小于指定交易量的数据
        if min_volume:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["funda_volume"]) > min_volume
            }
        if len(fields):
            data = {
                k: data[k]
                for k in data
                if data[k]["coupon_descr_s"] in "".join(fields)
            }
        if ignore_nodown:
            data = {
                k: data[k]
                for k in data
                if data[k]["fund_descr"].find("无下折") == -1
            }
        if forever:
            data = {
                k: data[k]
                for k in data
                if data[k]["funda_left_year"].find("永续") != -1
            }
        if min_discount:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["funda_discount_rt"][:-1]) > min_discount
            }

        self.__funda = data
        return self.__funda

    def fundm(self):
        """以字典形式返回分级母基数据
        """
        # 添加当前的ctime
        self.__fundm_url = self.__fundm_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__fundm_url)
        # 获取返回的json字符串
        fundmjson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatfundajson(fundmjson)
        self.__fundm = data
        return self.__fundm

    def fundb(self, fields=None, min_volume=0, min_discount=0, forever=False):
        """以字典形式返回分级B数据
        :param fields:利率范围，形如['+3.0%', '6.0%']
        :param min_volume:最小交易量，单位万元
        :param min_discount:最小折价率, 单位%
        :param forever: 是否选择永续品种,默认 False
        """
        if fields is None:
            fields = []
        # 添加当前的ctime
        self.__fundb_url = self.__fundb_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__fundb_url)
        # 获取返回的json字符串
        fundbjson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatfundbjson(fundbjson)
        # 过滤小于指定交易量的数据
        if min_volume:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["fundb_volume"]) > min_volume
            }
        if len(fields):
            data = {
                k: data[k]
                for k in data
                if data[k]["coupon_descr_s"] in "".join(fields)
            }
        if forever:
            data = {
                k: data[k]
                for k in data
                if data[k]["fundb_left_year"].find("永续") != -1
            }
        if min_discount:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["fundb_discount_rt"][:-1]) > min_discount
            }
        self.__fundb = data
        return self.__fundb

    def fundarb(
        self,
        jsl_username,
        jsl_password,
        avolume=100,
        bvolume=100,
        ptype="price",
    ):
        """以字典形式返回分级A数据
        :param jsl_username: 集思录用户名
        :param jsl_password: 集思路登录密码
        :param avolume: A成交额，单位百万
        :param bvolume: B成交额，单位百万
        :param ptype: 溢价计算方式，price=现价，buy=买一，sell=卖一
        """
        session = requests.session()
        headers = {
            # pylint: disable=line-too-long
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
        }
        session.headers.update(headers)

        logindata = dict(
            return_url="http://www.jisilu.cn/",
            user_name=jsl_username,
            password=jsl_password,
            net_auto_login="1",
            _post_type="ajax",
        )

        rep = session.post(self.__jsl_login_url, data=logindata)

        if rep.json()["err"] is not None:
            return rep.json()

        # 添加当前的ctime
        fundarb_url = self.__fundarb_url.format(ctime=int(time.time()))

        pdata = dict(
            avolume=avolume,
            bvolume=bvolume,
            ptype=ptype,
            is_search="1",
            market=["sh", "sz"],
            rp="50",
        )
        # 请求数据
        rep = session.post(fundarb_url, data=pdata)

        # 获取返回的json字符串
        fundajson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatfundajson(fundajson)

        self.__fundarb = data
        return self.__fundarb

    def etfindex(
        self, index_id="", min_volume=0, max_discount=None, min_discount=None
    ):
        """
        以字典形式返回 指数ETF 数据
        :param index_id: 获取指定的指数
        :param min_volume: 最小成交量
        :param min_discount: 最低溢价率, 适用于溢价套利, 格式 "-1.2%", "-1.2", -0.012 三种均可
        :param max_discount: 最高溢价率, 适用于折价套利, 格式 "-1.2%", "-1.2", -0.012 三种均可
        :return: {"fund_id":{}}
        """
        # 添加当前的ctime
        etf_index_url = self.__etf_index_url.format(ctime=int(time.time()))
        # 请求数据
        etf_json = requests.get(etf_index_url).json()

        # 格式化返回的json字符串
        data = self.formatetfindexjson(etf_json)

        # 过滤
        if index_id:
            # 指定跟踪的指数代码
            data = {
                fund_id: cell
                for fund_id, cell in data.items()
                if cell["index_id"] == index_id
            }
        if min_volume:
            # 过滤小于指定交易量的数据
            data = {
                fund_id: cell
                for fund_id, cell in data.items()
                if float(cell["volume"]) >= min_volume
            }
        if min_discount is not None:
            # 指定最小溢价率
            if isinstance(min_discount, str):
                if min_discount.endswith("%"):
                    # 如果是字符串形式,先转为浮点形式
                    min_discount = self.percentage2float(min_discount)
                else:
                    min_discount = float(min_discount) / 100.
            data = {
                fund_id: cell
                for fund_id, cell in data.items()
                if self.percentage2float(cell["discount_rt"]) >= min_discount
            }
        if max_discount is not None:
            # 指定最大溢价率
            if isinstance(max_discount, str):
                if max_discount.endswith("%"):
                    # 如果是字符串形式,先转为浮点形式
                    max_discount = self.percentage2float(max_discount)
                else:
                    max_discount = float(max_discount) / 100.
            data = {
                fund_id: cell
                for fund_id, cell in data.items()
                if self.percentage2float(cell["discount_rt"]) <= max_discount
            }

        self.__etfindex = data
        return self.__etfindex

    def qdii(self, min_volume=0):
        """以字典形式返回QDII数据
        :param min_volume:最小交易量，单位万元
        """
        # 添加当前的ctime
        self.__qdii_url = self.__qdii_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__qdii_url)
        # 获取返回的json字符串
        fundjson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatjisilujson(fundjson)
        data = {x: y for x, y in data.items() if y["notes"] != "估值有问题"}
        # 过滤小于指定交易量的数据
        if min_volume:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["volume"]) > min_volume
            }

        self.__qdii = data
        return self.__qdii

    # pylint: disable=invalid-name
    def cb(self, min_volume=0):
        """以字典形式返回QDII数据
        :param min_volume:最小交易量，单位万元
        """
        # 添加当前的ctime
        self.__cb_url = self.__cb_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__cb_url)
        # 获取返回的json字符串
        fundjson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatjisilujson(fundjson)
        # 过滤小于指定交易量的数据
        if min_volume:
            data = {
                k: data[k]
                for k in data
                if float(data[k]["volume"]) > min_volume
            }

        self.__cb = data
        return self.__cb


if __name__ == "__main__":
    Jsl().etfindex(
        index_id="000016",
        min_volume=0,
        max_discount="-0.4",
        min_discount="-1.3%",
    )

# 导入tushare
import os
import sqlite3

import pandas as pd
import tushare as ts


class SqliteMgr:
    def __init__(self):
        self.db = "data.db"
        self.conn = sqlite3.connect(self.db)

    def df_2_db(self, df, tb):
        df.to_sql(tb, self.conn, if_exists="replace", index=False)

    def db_2_df(self, sql):
        df = pd.read_sql(sql, self.conn)
        return df

    def execute(self, sql):
        return self.conn.execute(sql)


# 初始化pro接口
class TSMgr:
    def __init__(self):
        self.pro = ts.pro_api(
            "854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c"
        )

    def get_index_basic(self):
        # 拉取数据
        df = self.pro.index_basic(
            **{
                # "ts_code":{'$in':codes},
                "market": "",
                "publisher": "",
                "category": "",
                "name": "",
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "name",
                "market",
                "publisher",
                "category",
                "base_date",
                "base_point",
                "list_date",
            ]
        )
        return df

    def get_etf_basic(self):
        # 拉取数据
        df = self.pro.fund_basic(
            **{
                "ts_code": "",
                "market": "E",
                "update_flag": "",
                "offset": "",
                "limit": "",
                "status": "L",
                "fund_type": "",
            },
            fields=[
                "ts_code",
                "name",
                "management",
                "custodian",
                "fund_type",
                "found_date",
                "due_date",
                "list_date",
                "issue_date",
                "delist_date",
                "issue_amount",
                "m_fee",
                "c_fee",
                "duration_year",
                "p_value",
                "min_amount",
                "exp_return",
                "benchmark",
                "status",
                "invest_type",
                "type",
                "trustee",
                "purc_startdate",
                "redm_startdate",
                "market",
            ]
        )
        return df

    def get_index_quotes(self, code):
        # 拉取数据
        df = self.pro.index_daily(
            **{
                "ts_code": code,
                "trade_date": "",
                "start_date": "",
                "end_date": "",
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "trade_date",
                "close",
                "open",
                "high",
                "low",
                "pre_close",
                "change",
                "pct_chg",
                "vol",
                "amount",
            ]
        )
        return df

    def get_global_index_quotes(self, code):
        # 拉取数据
        df = self.pro.index_global(
            **{
                "ts_code": code,
                "trade_date": "",
                "start_date": "",
                "end_date": "",
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "trade_date",
                "open",
                "close",
                "high",
                "low",
                "pre_close",
                "change",
                "pct_chg",
                "swing",
                "vol",
            ]
        )
        return df

    def get_etf_quotes(self, code):
        df = self.pro.fund_daily(
            **{
                "trade_date": "",
                "start_date": "",
                "end_date": "",
                "ts_code": code,
                "limit": "",
                "offset": "",
            },
            fields=[
                "ts_code",
                "trade_date",
                "pre_close",
                "open",
                "high",
                "low",
                "close",
                "change",
                "pct_chg",
                "vol",
                "amount",
            ]
        )
        return df

    def build_all_index_quotes(self):
        codes = [
            "000300.SH",
            "000905.SH",
            "399006.SZ",  # 创业板
            "000852.SH",  # 中证1000
            "399324.SZ",  # 深证红利
            "000922.SH",  # 中证红利
            "399997.SZ",  # 中证白酒
            "399396.SZ",  # 食品饮料
            "000013.SH",  # 上证企债
            "000016.SH",  # 上证50
        ]
        for code in codes:
            df = self.get_index_quotes(code)
            print(code)
            df.to_csv("indexes/" + code + ".csv")
            # SqliteMgr().df_2_db(df, 'index_quotes')

    def build_all_globe_index_quotes(self):
        codes = {
            "HSI": "恒生指数",
            "SPX": "标准普尔500指数",
            "IXIC": "纳斯达克指数",
            "GDAXI": "德国DAX指数",
            "N225": "日经225指数",
        }
        for code in codes:
            df = self.get_global_index_quotes(code)
            print(code)
            df.to_csv("indexes/" + code + ".csv")

    def build_all_etf_quotes(self):
        db = SqliteMgr()
        df_codes = db.db_2_df("select ts_code from etf")
        for code in list(df_codes["ts_code"]):
            filename = "etfs/" + code + ".csv"
            if not os.path.exists(filename):
                df = self.get_etf_quotes(code)
                print(code)
                df.to_csv(filename)


if __name__ == "__main__":
    _ts = TSMgr()

    # _ts.build_all_etf_quotes()
    # _ts.build_all_globe_index_quotes()
    _ts.build_all_index_quotes()

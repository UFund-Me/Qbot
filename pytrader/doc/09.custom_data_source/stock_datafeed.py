import datetime
import traceback
import pymysql

from backtrader.feed import DataBase
from backtrader import date2num


class MySQLData(DataBase):
    params = (
        ('fromdate', datetime.datetime.min),
        ('todate', datetime.datetime.max),
        ('ts_code', ''),
    )
    lines = (
        "turnover",
        "turnover_rate"
    )

    def load_data_from_db(self, table, ts_code, start_time, end_time):
        """
        从MySQL加载指定数据
        Args:
            table (str): 表名
            ts_code (str): 股票代码
            start_time (str): 起始时间
            end_time (str): 终止时间
        return:
            data (List): 数据集
        """
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="12345678",
            db="golden_stone",
            port=3306
        )

        cur = db.cursor()
        sql = cur.execute(
            f"SELECT * FROM {table} WHERE trade_time >= '{start_time}'"
            "and trade_time < '{end_time}' and ts_code = '{ts_code}' order by trade_time asc"
        )
        data = cur.fetchall()
        db.close()
        return iter(list(data))

    def __init__(self, *args, **kwargs):
        self.result = []
        self.empty = False

    def start(self):
        self.result = self.load_data_from_db(
            "stock_normalk", self.p.ts_code, self.p.fromdate, self.p.todate
        )

    def _load(self):
        if self.empty:
            return False
        try:
            one_row = next(self.result)
        except StopIteration:
            return False
        self.lines.datetime[0] = date2num(one_row[3])
        self.lines.open[0] = float(one_row[4])
        self.lines.high[0] = float(one_row[5])
        self.lines.low[0] = float(one_row[6])
        self.lines.close[0] = float(one_row[7])
        self.lines.volume[0] = float(one_row[8])
        self.lines.turnover[0] = float(one_row[9])
        self.lines.turnover_rate[0] = float(one_row[12])
        return True

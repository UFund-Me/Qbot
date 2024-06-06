import pandas as pd
from datetime import datetime
import os
import backtrader as bt

from qbot.common.logger import LOGGER as logger
from qbot.engine.config import DATA_DIR_CSV

def load_data(code):
    filename = '{}/{}.csv'.format(DATA_DIR_CSV, code)
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df['date'] = df['date'].apply(lambda x: str(x))
        df.set_index('date', inplace=True)
        df.sort_index(ascending=True, inplace=True)
        df.dropna(inplace=True)
    else:
        logger.error(f'load_from_file error: {filename} is not exist.')
        return None
    return df


df = load_data('000300.SH')
df_spx = load_data('SPX')

def to_backtrader_dataframe(df):
    df.index = pd.to_datetime(df.index)
    df['openinterest'] = 0
    if 'amount' not in df.columns:
        df['amount'] = 0
    df = df[['open', 'high', 'low', 'close', 'volume','amount', 'openinterest']]
    return df


df = to_backtrader_dataframe(df)
df = df[df.index > '20110708']

df_spx = to_backtrader_dataframe(df=df_spx)

#print(df[['close']])
#print(df_spx[['close']])

class PandasData_more(bt.feeds.PandasData):
    lines = ('amount', ) # 要添加的线
    # 设置 line 在数据源上的列位置
    params = (
        ('amount', -1),
    )
    # -1表示自动按列明匹配数据，也可以设置为线在数据源中列的位置索引 (('pe',6),('pb',7),)


# 实例化 cerebro
cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)

start = datetime(2011, 7, 8)
end = datetime.now().date()
data = PandasData_more(dataname=df, name='000300', fromdate=start, todate=end)
cerebro.adddata(data)  # Add the data feed
cerebro.adddata(PandasData_more(dataname=df_spx, name='SPX', fromdate=start, todate=end))
# print(df)
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')  # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')  # 年化收益率
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio')  # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')  # 回撤


# 通过继承 Strategy 基类，来构建自己的交易策略子类
class MyStrategy(bt.Strategy):
    # 定义我们自己写的这个 MyStrategy 类的专有属性
    def __init__(self):
        '''必选，策略中各类指标的批量计算或是批量生成交易信号都可以写在这里'''
        print(self.datas)
        print(self.data0)
        print(self.data1)
        print(self.datas[0])
        print(self.getdatabyname('SPX'))
        print('line aliases', self.data0.getlinealiases())
        # print('lines', len(self.data0.lines),self.data0.lines[0])
        # print('data0.lines.open', len(self.data0.lines), self.data0.open)
        # print('data0.lines.close', self.data0[-1], self.data0.close[-1])
        # print('data0.lines.datetime', self.data0.datetime)
        self.i = 0

    # 构建交易函数: 策略交易的主体部分
    def next(self):
        if self.i == 0:
            self.i += 1
            print('line的长度', self.data0.buflen(), self.data1.buflen())
            print('添加的列amount', self.data0.amount[0])
            print(self.datas[0]._name)
            print('datetime的使用', self.data0.datetime[0], bt.num2date(self.data0.datetime[0]).date(),
                  self.data0.datetime.date(0), self.data0.datetime.date(1))
            print(self.data1.close[1], self.data1.datetime.date(-5), self.data1.lines.datetime.date(0))
            print('next===>data0.lines.close', self.data.datetime.date(0), self.datas[0].close[0], self.data[-1],
                  self.data[-2])
            print('get====>data0.lines.close', self.data0.datetime.date(0), self.data0.get(ago=0, size=2))

        # self.buy()
        pass
        '''必选，在这里根据交易信号进行买卖下单操作'''
        # print(self.data.close[0])

class MyStockCommissionScheme(bt.CommInfoBase):
    '''
    1.佣金按照百分比。
    2.每一笔交易有一个最低值，比如5块，当然有些券商可能会免5.
    3.卖出股票还需要收印花税。
    4.可能有的平台还需要收平台费。
    '''
    params = (
        ('stampduty', 0.005),  # 印花税率
        ('commission', 0.005),  # 佣金率
        ('stocklike', True),#股票类资产，不考虑保证金
        ('commtype', bt.CommInfoBase.COMM_PERC),#按百分比
        ('minCommission', 5),#最小佣金
        ('platFee', 0),#平台费用
    )

    def _getcommission(self, size, price, pseudoexec):
        '''
        size>0，买入操作。
        size<0，卖出操作。
        '''
        if size > 0:  # 买入，不考虑印花税，需要考虑最低收费
            return max(size * price * self.p.commission,self.p.minCommission)+platFee
        elif size < 0:  # 卖出，考虑印花税。
            return max(abs(size) * price * self.p.commission,self.p.minCommission)+abs(size) * price * self.p.stampduty+platFee
        else:
            return 0  # 防止特殊情况下size为0.

cerebro.broker.setcommission(0.0003)
cerebro.broker.addcommissioninfo(MyStockCommissionScheme())
print("当前现金：", cerebro.broker.getcash())
print('当前总资产：',cerebro.broker.getvalue())
cerebro.broker.set_slippage_perc(0.0001)
cerebro.broker.set_slippage_fixed(0.03)
cerebro.adddata(bt.feeds.PandasData(dataname=df, name='000300'))
cerebro.addstrategy(MyStrategy)

results = cerebro.run()

strat = results[0]
# 返回日度收益率序列
daily_return = pd.Series(strat.analyzers.pnl.get_analysis())
# 打印评价指标
print("--------------- AnnualReturn -----------------")
print(strat.analyzers._AnnualReturn.get_analysis())
print("--------------- SharpeRatio -----------------")
print(strat.analyzers._SharpeRatio.get_analysis())
print("--------------- DrawDown -----------------")
print(strat.analyzers._DrawDown.get_analysis())

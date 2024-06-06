import pandas as pd
from qbot.common.logger import LOGGER as logger
from qbot.engine.config import DATA_DIR_CSV

import os
import backtrader as bt

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
# df_spx = load_data('spx')


def to_backtrader_dataframe(df):
    df.index = pd.to_datetime(df.index)
    df['openinterest'] = 0
    if 'amount' not in df.columns:
        df['amount'] = 0
    df = df[['open', 'high', 'low', 'close', 'volume', 'amount', 'openinterest']]
    return df


df = to_backtrader_dataframe(df)

import backtrader as bt


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.broker.add_cash(1000)
        print('更新现金', self.broker.get_cash())
        self.size = 10
        self.value = 38.5
        self.percent = 26

    def next(self):
        print('当前可用资金', self.broker.getcash())
        print('当前总资产', self.broker.getvalue())
        print('当前持仓量', self.broker.getposition(self.data).size)
        print('当前持仓成本', self.broker.getposition(self.data).price)
        # 也可以直接获取持仓
        print('当前持仓量', self.getposition(self.data).size)
        print('当前持仓成本', self.getposition(self.data).price)
        # 注：getposition() 需要指定具体的标的数据集
        self.buy(exectype=bt.Order.Market)

        # 按目标数量下单
        self.order = self.order_target_size(target=self.size)
        # 按目标金额下单
        self.order = self.order_target_value(target=self.value)
        # 按目标百分比下单
        self.order = self.order_target_percent(target=self.percent)


cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)

class MyStockCommissionScheme(bt.CommInfoBase):
    def __init__(self):
        '''
        1.佣金按照百分比。
        2.每一笔交易有一个最低值，比如5块，当然有些券商可能会免5.
        3.卖出股票还需要收印花税。
        4.可能有的平台还需要收平台费。
        '''
        self.params = (
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
        platFee = self.params['platFee']
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

cerebro.run()

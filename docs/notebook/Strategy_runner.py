from datetime import datetime
import backtrader as bt
import pandas as pd
import os
import tushare as ts
import matplotlib
import matplotlib.pyplot as plt
from stock_api import get_daily
matplotlib.use('agg')
data_path = './data/'
if not os.path.exists(data_path):
    os.makedirs(data_path)
mytoken = '565ee6d69fb85cb0bc7fdfc8dea4b8ce1f18366f30e8d23a253bb9cf'


class Strategy_runner:
    def __init__(self,
                 strategy,
                 ts_code,
                 start_date,
                 end_date,
                 data_path=data_path,
                 pro=True,
                 token=mytoken):
        ts.set_token(mytoken)
        pro = ts.pro_api()
        self.ts_code = ts_code
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path
        # convert to datetime
        self.start_datetime = datetime.strptime(start_date, '%Y%m%d')
        self.end_datetime = datetime.strptime(end_date, '%Y%m%d')
        df = self.read_save(self.ts_code, pro)
        self.df_bt = self.preprocess(df, pro)
        self.strategy = strategy
        self.cerebro = bt.Cerebro()

    def read_save(self, ts_code, pro=True):
        if pro:
            csv_name = f'pro_day_{str(ts_code)}-{str(self.start_date)}-{str(self.end_date)}.csv'
        else:
            csv_name = f'day_{str(ts_code)}-{str(self.start_date)}-{str(self.end_date)}.csv'
        csv_path = os.path.join(self.data_path, csv_name)
        if os.path.exists(csv_path):
            if pro:
                df = pd.read_csv(csv_path)
            else:
                df = pd.read_csv(csv_path, index_col=0)
        else:
            if pro:
                # self.pro = ts.pro_api()
                # self.df = self.pro.daily(ts_code=self.ts_code, start_date=self.start_date, end_date=self.end_date)
                df = get_daily(ts_code, self.start_date, self.end_date)
                if not df.empty:
                    df.to_csv(csv_path, index=False)
            else:
                df = ts.get_hist_data(ts_code, str(self.start_datetime),
                                      str(self.end_datetime))
                if not df.empty:
                    df.to_csv(csv_path, index=True)
        return df

    def preprocess(self, df, pro=False):
        if pro:
            features = ['open', 'high', 'low', 'close', 'vol', 'trade_date']
            # convert_datetime = lambda x:datetime.strptime(x,'%Y%m%d')
            convert_datetime = lambda x: pd.to_datetime(str(x))
            df['trade_date'] = df['trade_date'].apply(convert_datetime)
            bt_col_dict = {'vol': 'volume', 'trade_date': 'datetime'}
            df = df.rename(columns=bt_col_dict)
            df = df.set_index('datetime')
            # df.index = pd.DatetimeIndex(df.index)
        else:
            features = ['open', 'high', 'low', 'close', 'volume']
            df = df[features]
            df['openinterest'] = 0
            df.index = pd.DatetimeIndex(df.index)

        df = df[::-1]
        return df

    def run(self):
        data = bt.feeds.PandasData(dataname=self.df_bt,
                                   fromdate=self.start_datetime,
                                   todate=self.end_datetime)
        self.cerebro.adddata(data)  # Add the data feed
        self.cerebro.addstrategy(self.strategy)  # Add the trading strategy
        # self.cerebro.broker.setcash(1000.0)
        # self.cerebro.addsizer(bt.sizers.FixedSize, stake=100)
        self.cerebro.broker.setcommission(commission=0.0)  # 佣金
        self.cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
        self.cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
        self.results = self.cerebro.run()
        strat = self.results[0]
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        print('SR:', strat.analyzers.SharpeRatio.get_analysis())
        print('DW:', strat.analyzers.DW.get_analysis())
        return self.cerebro, strat

    def plot(self, iplot=False):
        plt.rcParams['figure.figsize'] = [15, 8]
        self.cerebro.plot(iplot=iplot)


def test():
    from SmaCross import SmaCross
    ts_code = '600515.SH'
    start_date = '20190101'
    end_date = '20191231'
    strategy_runner = Strategy_runner(strategy=SmaCross,
                                      ts_code=ts_code,
                                      start_date=start_date,
                                      end_date=end_date,
                                      pro=True)
    results = strategy_runner.run()
    strategy_runner.plot()
    return results


if __name__ == '__main__':
    test()

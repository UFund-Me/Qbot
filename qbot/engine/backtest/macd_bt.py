import backtrader as bt
import pandas as pd
import tushare as ts


class MyStrategy(bt.Strategy):
    params = (
        ("fast", 5),  # 快速移动平均线的周期
        ("slow", 20),  # 慢速移动平均线的周期
    )

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.fast,
            plotname="5 day moving average",  # 计算快速移动平均线
        )
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.slow,
            plotname="20 day moving average",  # 计算慢速移动平均线
        )
        self.crossover = bt.indicators.CrossOver(
            self.fast_moving_average, self.slow_moving_average
        )  # 计算交叉点

    def next(self):
        if not self.position:
            if self.crossover > 0:  # 如果快速移动平均线上穿慢速移动平均线
                amount_to_invest = 0.95 * self.broker.cash  # 计算可投资金额
                self.size = int(
                    amount_to_invest / self.data.close
                )  # 计算可购买股票数量
                print(
                    "Buy {} shares of {} at {}".format(
                        self.size, "600519", self.data.close[0]
                    )
                )  # 输出购买信息
                self.buy(size=self.size)  # 买入股票
        else:
            if self.crossover < 0:  # 如果快速移动平均线下穿慢速移动平均线
                print(
                    "Sell {} shares of {} at {}".format(
                        self.size, "600519", self.data.close[0]
                    )
                )  # 输出卖出信息
                self.close()  # 卖出股票


if __name__ == "__main__":
    cerebro = bt.Cerebro()  # 创建Cerebro引擎
    cerebro.addstrategy(MyStrategy)  # 添加策略
    symbol = "600519"  # 股票代码
    df = ts.get_k_data(symbol, start="2018-01-01", end="2023-03-20")  # 获取股票数据
    df["date"] = pd.to_datetime(df["date"])  # 将日期转换为datetime格式
    df = df.set_index("date", drop=True)  # 将日期设置为索引
    data = bt.feeds.PandasData(
        dataname=df,
        datetime=None,
        open=0,
        high=1,
        low=2,
        close=3,
        volume=4,
        openinterest=-1,
    )  # 创建数据源
    cerebro.adddata(data)  # 添加数据源
    cerebro.broker.setcash(1000000.0)  # 设置初始资金
    cerebro.broker.setcommission(commission=0.001)  # 设置佣金
    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())  # 输出初始资金
    cerebro.run()  # 运行策略
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())  # 输出最终资金
    cerebro.plot()  # 绘制图表

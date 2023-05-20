from collections import defaultdict

import pandas as pd


class Account:
    def __init__(self, init_cash=100000.0):
        self.init_cash = init_cash
        self.curr_cash = self.init_cash
        self.curr_holding = defaultdict(float)  # 当前持仓{symbol:mv}

        self.cache_dates = []
        self.cache_portfolio_mv = []

    # 要更新一次df_bar及市值，再进行交易。
    def update_bar(self, date, df_bar):

        # 所以有持仓的，按收益率更新mv
        total_mv = 0.0
        # 当前已经持仓中标的，使用收盘后的收益率更新
        for s, mv in self.curr_holding.items():
            rate = 0.0
            # 这里不同市场，比如海外市场，可能不存在的，不存在变化率就是0.0， 即不变
            if s in df_bar.index:
                symbol_bar = df_bar.loc[s]
                rate = symbol_bar["rate"]

            new_mv = mv * (1 + rate)
            self.curr_holding[s] = new_mv
            total_mv += new_mv

        self.cache_portfolio_mv.append(total_mv + self.curr_cash)
        self.cache_dates.append(date)

    # 持仓市值，不包括cash
    def _calc_total_holding_mv(self):
        total_mv = 0.0
        for s, mv in self.curr_holding.items():
            total_mv += mv
        return total_mv

    # weights之和需要=1，空仓就是cash:1，只调整curr_holding/cash两个变量
    def adjust_weights(self, date, weights):
        total_mv = self._calc_total_holding_mv()
        total_mv += self.curr_cash

        # 再平衡时，可能就是keys相同，不用调整
        if set(weights.keys()) == set(self.curr_holding.keys()):

            b_adjust = True
            if len(weights.items()) > 0:
                for s, w in weights.items():
                    curr_w = self.curr_holding[s] / total_mv

                    if abs(w - curr_w) > 0.01:
                        b_adjust = True
            else:
                b_adjust = False

            if b_adjust is False:
                # print('仓位相同...不调整')
                return
        if len(weights.items()) == 0:
            print("账户需要清仓!")
        old_pos = self.curr_holding.copy()
        self.curr_holding.clear()
        for s, w in weights.items():
            self.curr_holding[s] = total_mv * w

        self.curr_cash = total_mv - self._calc_total_holding_mv()
        print(date, "from:", old_pos, "-->to:", self.curr_holding)
        # date, from old_pos -> new_pos

    def run(self, algo_list):
        self.algo_list = algo_list
        for index, date in enumerate(self.dates):
            self.curr_date = date
            self.step(index, date)

    def step(self, index, date):
        return_se = self._get_curr_return_se(date)
        self.acc.update_bar(date, return_se)
        self.algo_processor()

    def algo_processor(self):
        context = {'engine': self, 'acc': self.acc}
        for algo in self.algo_list:
            if algo(context) is True:  # 如果algo返回True,直接不运行，本次不调仓
                return None

    # def get_results_df(self):
    #     df = pd.DataFrame({'date': self.acc.cache_dates, 'portfolio': self.acc.cache_portfolio_mv})
    #     df['rate'] = df['portfolio'].pct_change()
    #     df['equity'] = (df['rate'] + 1).cumprod()
    #     df.set_index('date', inplace=True)
    #     df.dropna(inplace=True)
    #     return df

    def get_results_df(self):
        df = pd.DataFrame(
            {"date": self.cache_dates, "portfolio": self.cache_portfolio_mv}
        )
        df["rate"] = df["portfolio"].pct_change()
        df['equity'] = (df['rate'] + 1).cumprod()
        df.index = df["date"]
        df.dropna(inplace=True)
        return df

    # 一些对外提供接口的能力
    def get_holding_instruments(self):
        return list(self.curr_holding.keys())

    def get_total_mv(self):
        return self._calc_total_holding_mv() + self.curr_cash

from datetime import datetime

import pandas as pd


class PerformanceUtils(object):
    def rate2equity(self, df_rates):
        df = df_rates.copy(deep=True)
        df.dropna(inplace=True)
        for col in df.columns:
            df[col] = (df[col] + 1).cumprod()
        return df

    def equity2rate(self, df_equity):
        df = df_equity.copy(deep=True)
        df = df.pct_change()
        return df

    def calc_equity(self, df_equity):
        df_rates = self.equity2rate(df_equity)
        return self.calc_rates(df_rates)

    def calc_rates(self, df_rates):
        df_equity = self.rate2equity(df_rates)
        df_rates.dropna(inplace=True)
        df_equity.dropna(inplace=True)
        # 累计收益率，年化收益
        count = len(df_rates)
        accu_return = round(df_equity.iloc[-1] - 1, 3)
        annu_ret = round((accu_return + 1) ** (252 / count) - 1, 3)
        # 标准差
        std = round(df_rates.std() * (252 ** 0.5), 3)
        # 夏普比
        sharpe = round(annu_ret / std, 3)
        # 最大回撤
        mdd = round((df_equity / df_equity.expanding(min_periods=1).max()).min() - 1, 3)

        ret_2_mdd = round(annu_ret / abs(mdd), 3)

        ratios = [accu_return, annu_ret, std, sharpe, mdd, ret_2_mdd]

        # df_ratio存放这里计算结果
        df_ratios = pd.concat(ratios, axis=1)
        # df_ratios.index = list(df_rates.columns)
        df_ratios.columns = ["累计收益", "年化收益", "波动率", "夏普比", "最大回撤", "年化收益与最大回撤比"]

        # 相关系数矩阵
        df_corr = round(df_equity.corr(), 2)

        start_dt = df_rates.index[0]
        end_dt = df_rates.index[-1]
        if isinstance(start_dt, str):
            start_year = int(start_dt[:4])
            end_year = int(end_dt[:4])
            df_equity["date"] = df_equity.index
            df_equity.index = df_equity["date"].apply(
                lambda x: datetime.strptime(x, "%Y%m%d")
            )
            del df_equity["date"]
        else:
            start_year = start_dt[:4]
            end_year = end_dt.year

        years = []
        for year in range(start_year, end_year + 1):
            sub_df = df_equity.loc[str(year)]
            if len(sub_df) <= 3:
                continue
            year_se = round(sub_df.iloc[-1] / sub_df.iloc[0] - 1, 3)
            year_se.name = str(year)
            years.append(year_se)
        if len(years):
            df_years = pd.concat(years, axis=1)
        else:
            df_years = None
        return df_ratios, df_corr, df_years

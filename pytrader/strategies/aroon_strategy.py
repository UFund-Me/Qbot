'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-05-08 22:08:13
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-05-08 22:08:13
FilePath: /Qbot/pytrader/strategies/aroon_strategy.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

class AroonStrategy(TemplateStrategy):
    params = (("start_date", None), ('end_date', None),)

    def __init__(self):
        super().__init__()
        # 基本配置
        self.max_hold = 5
        self.this_month = self.params.start_date.month
        total_bond_code = []
        for this_data in self.datas:
            if type(this_data).__name__ == "StockData":
                total_bond_code.append(this_data._name)
        self.total_bond_code = total_bond_code
        self.vic_dict = {'801210.SI': 0, '801110.SI': 1, '801750.SI': 2, '801120.SI': 3, '801890.SI': 4, '801080.SI': 5,
                         '801200.SI': 6, '801140.SI': 7, '801160.SI': 8, '801730.SI': 9, '801010.SI': 10,
                         '801130.SI': 11, '801760.SI': 12, '801770.SI': 13, '801050.SI': 14, '801040.SI': 15,
                         '801180.SI': 16, '801720.SI': 17, '801710.SI': 18, '801030.SI': 19, '801880.SI': 20,
                         '801170.SI': 21, '801790.SI': 22, '801150.SI': 23, '801230.SI': 24, '801740.SI': 25,
                         '801950.SI': 26, '801780.SI': 27}

    def next(self):
        """最核心的触发策略"""
        hold_bond_name = [_p._name for _p in self.broker.positions if self.broker.getposition(_p).size > 0]  # 查看持仓
        # 计算指标
        _candidate_dict = {}
        for _candidate_code in self.total_bond_code:
            _candidate_dict[_candidate_code] = {
                "aroondown": self.getdatabyname(_candidate_code).aroondown[0],
                "aroonup": self.getdatabyname(_candidate_code).aroonup[0],
            }
        candidate_df = pd.DataFrame(_candidate_dict).T
        candidate_df['aroo_energy'] = candidate_df['aroondown'] + candidate_df['aroonup']
        candidate_df['aroo_mines'] = candidate_df['aroonup'] - candidate_df['aroondown']
        candidate_df = pd.merge(candidate_df, pd.DataFrame(self.vic_dict, index=['rank']).T,
                                left_index=True, right_index=True)
        candidate_df = candidate_df.sort_values(['aroo_mines', "rank"], ascending=[False, True])

        if candidate_df['aroo_energy'].sum() == 0:
            return
        if len(hold_bond_name) < self.max_hold:
            self.get_buy_bond(candidate_df, self.max_hold - len(hold_bond_name))
        # 卖出的逻辑
        for _index, _series in candidate_df.iterrows():
            if _index in hold_bond_name:
                if _series['aroonup'] < _series['aroondown']:
                    self.sell(data=_index, size=self.getpositionbyname(_index).size,
                              valid=self.getdatabyname(_index).datetime.date(1))

    def get_buy_bond(self, candidate_df, buy_num):
        hold_bond_name = [_p._name for _p in self.broker.positions if self.broker.getposition(_p).size > 0]
        for index, series in candidate_df.iterrows():
            if series["aroo_energy"] <= 50:  # 当 AroonDown + AroonUp > 50时才执行判操作
                continue
            if index in hold_bond_name:
                continue
            buy_data = self.getdatabyname(index)
            if len(buy_data) >= buy_data.buflen():
                continue
            if series['aroonup'] > series['aroondown']:
                buy_cost_value = self.broker.getcash() / (self.max_hold - len(hold_bond_name)) * (
                        1 - self.broker.comminfo[None].p.commission)
                buy_size = buy_cost_value / self.getdatabyname(index).close[0]
                self.buy(data=buy_data, size=buy_size, exectype=bt.Order.Limit,
                         price=buy_data.close[0],
                         valid=buy_data.datetime.date(1))
                logger.debug("买入 {} size:{} 预计费用:{}".format(index, buy_size, buy_cost_value))
                buy_num -= 1
            if buy_num == 0:
                break

    def stop(self):
        # 绘制净值曲线
        wealth_curve_data = {}
        for _k, _v in self.value_record.items():
            wealth_curve_data[_k] = _v / self.broker.startingcash
        self.plot_wealth_curve(wealth_curve_data, "arron_{}_{}".format(
            self.params.start_date.strftime("%Y-%m-%d"), self.params.end_date.strftime("%Y-%m-%d")))
        # 最终结果
        daily_return = cal_daily_return(pd.Series(self.value_record))
        _, record_dict = cal_rolling_feature(daily_return)
        print(record_dict)
        print('a')

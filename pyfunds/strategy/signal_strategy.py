import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('004933.xlsx', skiprows=3)  # 读取标的基金数据，跳过表头
buy_list = [0.00260]  # 买入下跌幅度列表
rev_list = []  # 初始化收益率列表
for rate in buy_list:  # 遍历每一个下跌幅度
    inv = 0  # 初始投资量为0
    cash = 1  # 初始账户现金为1
    total = 1  # 初始账户总额为1
    holding_days = 0  # 初始持有天数为0
    deal_num = 0  # 交易笔数
    inv_date = df.loc[len(df) - 1, 'Date']  # 初始假设投资日期为最后一天
    df.loc[0, 'vol'] = 0  # 成立日当天波动为0
    df.loc[0, 'inv'] = inv  # 成立日当天账户净值为1
    df.loc[0, 'cash'] = cash  # 成立日当天账户净值为1
    df.loc[0, 'total'] = total  # 成立日当天账户总额为1
    for i in df.index[1:]:  # 遍历索引
        vol = (df.loc[i, 'nav'] - df.loc[i-1, 'nav']) / df.loc[i-1, 'nav']  # 计算每日相对于前一日的波动
        if vol > 0.005 and df.loc[i-1, 'inv'] != 0 and holding_days >= 30:  # 如果涨幅大于0.5%且满仓且持有超30天
            inv = 0  # 空仓
            cash = df.loc[i-1, 'inv'] * (1 + vol)  # 现金为当天赎回值
        elif vol < -rate and df.loc[i-1, 'cash'] != 0:  # 如果跌幅大于0.5%且空仓
            inv = df.loc[i-1, 'cash']  # 持仓为前一天现金量
            cash = 0  # 满仓
            inv_date = df.loc[i, 'Date']  # 买入日期
            deal_num += 1  # 交易笔数加1
        else:
            inv = df.loc[i-1, 'inv'] * (1 + vol)  # 持仓为前一天持仓加波动
            cash = df.loc[i-1, 'cash']  # 现金为前一天现金
        holding_days = (df.loc[i, 'Date'] - inv_date).days  # 持有天数为当天减上次买入日期
        total = inv + cash  # 总量等于持仓加现金
        df.loc[i, 'vol'] = vol  # 波动率存储到DataFrame中
        df.loc[i, 'inv'] = inv  # 持仓存储到DataFrame中
        df.loc[i, 'cash'] = cash  # 现金存储到DataFrame中
        df.loc[i, 'total'] = total  # 总额存储到DataFrame中
    # for i, date in enumerate(df['Date']):  # 日期列不要时间只要日期
    #     df.loc[i, 'Date'] = date.to_pydatetime().date()
    rev = df.loc[len(df)-1, 'total'] - df.loc[0, 'total']  # 总收益率
    rev_list.append(rev)  # 加入收益率列表
    print('买入下跌幅度为%f时：' % rate)
    print('基金总收益为：{:.2%}'.format(df.loc[len(df)-1, 'nav'] - df.loc[0, 'nav']))
    print('基金波动率为：{:.2%}'.format(np.std(df['nav'])))
    print('策略总收益为：{:.2%}'.format(rev))
    print('策略波动率为：{:.2%}'.format(np.std(df['total'])))
    print('总交易日数：%d' % len(df))
    print('持币交易日共：%d个' % (df['cash'] > 0).sum())
    print('交易笔数：%d' % deal_num)
    print('平均下跌幅度：{:.2%}'.format(np.mean(df['vol'][df['vol'] < 0])))
    print('平均上涨幅度：{:.2%}'.format(np.mean(df['vol'][df['vol'] > 0])))
    print('--------------------分割线--------------------')
    df.to_excel('004933test.xlsx', index=None)  # 存储回测结果
plt.plot(buy_list, rev_list)
plt.show()
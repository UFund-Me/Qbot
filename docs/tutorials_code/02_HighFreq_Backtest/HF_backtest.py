from data_prepare import *

import warnings
warnings.filterwarnings("ignore")
from time import time


t0 = time()
code = 'CF2305'
start_date = '20230206'
end_date = '20230228'
freq = '10s'
balance = 1000000
multiplier = 5
pre_hold = 0
hold_time = 0    #当前持仓时间计数
fee = 0.00015   #单边交易手续费

####################数据准备#######################
print(str(pd.Timestamp.now()) +  '  加载数据')
tick_df = get_future_tick_resample(code, start_date, end_date, freq)
tick_df.dropna(inplace=True)
date_list = get_trade_date_list(start_date, end_date)
trade_df = tick_df
trade_df['MA5'] = trade_df['Close'].rolling(window=5).mean()
trade_df['MA20'] = trade_df['Close'].rolling(window=20).mean()
MA_S_arr = np.array(trade_df['MA5'])
MA_L_arr = np.array(trade_df['MA20'])
t1 = time()

####################策略逻辑#######################
print(str(pd.Timestamp.now()) +  '  开始回测')
trade_list = []
## 策略逻辑
for tk in range(1,trade_df.shape[0]):
    if pre_hold == 0:
        if (MA_S_arr[tk-2] < MA_L_arr[tk-2]) & (MA_S_arr[tk-1] > MA_L_arr[tk-1]) :   #开多1手
            trade = 1
            hold = 1
        elif (MA_S_arr[tk-2] > MA_L_arr[tk-2]) & (MA_S_arr[tk-1] < MA_L_arr[tk-1]) :  # 开空1手
            trade = -1
            hold = -1
        else:
            trade = 0
            hold = pre_hold
    else:
        if hold_time == 5:
            trade = -pre_hold
            hold = 0
            hold_time = 0
        else:
            hold_time += 1
            trade = 0
            hold = pre_hold
    trade_list.append(trade)
    pre_hold = hold
t2 = time()

####################交易清算#######################
trade_df['pre_cp'] = [trade_df['Close'].iloc[0]] + trade_df['Close'].iloc[:-1].tolist()
trade_df['cp'] = trade_df['Close']
trade_df['cp_chg'] = trade_df['Close'] - trade_df['pre_cp']

trade_df['trade'] = [0] + trade_list
trade_df['hold'] = trade_df['trade'].cumsum()
trade_df['pre_hold'] = [0] + trade_df['hold'].iloc[:-1].tolist()

trade_df['pnl'] = 0
trade_df['fee'] = 0
trade_df['trade_price'] = 0

idx = trade_df['hold'] != 0
trade_df.loc[idx,'pnl'] = trade_df.loc[idx,'hold'] * (trade_df.loc[idx,'price'] - trade_df.loc[idx,'pre_cp'])*multiplier

idx = trade_df['trade'] > 0
trade_df.loc[idx, 'trade_price'] = trade_df.loc[idx, 'Ask']
trade_df.loc[idx, 'fee'] = trade_df.loc[idx, 'trade'] * (trade_df.loc[idx, 'trade_price']) * multiplier * fee
idx1 = idx & (trade_df['pre_hold'] >= 0)   #开多
trade_df.loc[idx1, 'pnl'] = trade_df.loc[idx1, 'trade'] * (trade_df.loc[idx1, 'price'] - trade_df.loc[idx1, 'trade_price']) * multiplier - trade_df.loc[idx1, 'fee']
idx2 = idx & (trade_df['pre_hold'] < 0)  # 平空
trade_df.loc[idx2, 'pnl'] = trade_df.loc[idx2, 'pre_hold'] * (trade_df.loc[idx2, 'trade_price'] - trade_df.loc[idx2, 'pre_cp']) * multiplier - trade_df.loc[idx2, 'fee']

idx = trade_df['trade'] < 0
trade_df.loc[idx, 'trade_price'] = trade_df.loc[idx, 'Bid']
trade_df.loc[idx, 'fee'] = -trade_df.loc[idx, 'trade'] * (trade_df.loc[idx, 'trade_price']) * multiplier * fee
idx1 = idx & (trade_df['pre_hold'] > 0)  # 平多
trade_df.loc[idx1, 'pnl'] = trade_df.loc[idx1, 'pre_hold'] * (trade_df.loc[idx1, 'trade_price'] - trade_df.loc[idx1, 'pre_cp']) * multiplier - trade_df.loc[idx1, 'fee']
idx2 = idx & (trade_df['pre_hold'] <= 0)  # 开空
trade_df.loc[idx2, 'pnl'] = trade_df.loc[idx2, 'trade'] * (trade_df.loc[idx2, 'price'] - trade_df.loc[idx2, 'trade_price']) * multiplier - trade_df.loc[idx2, 'fee']

trade_df['cum_pnl'] = trade_df['pnl'].cumsum()
trade_df['cum_fee'] = trade_df['fee'].cumsum()
print(str(pd.Timestamp.now()) + ' pnl:' + str(trade_df['cum_pnl'].iloc[-1]).split('.')[0]+ ' fee:' + str(trade_df['cum_fee'].iloc[-1]).split('.')[0] +
      ' trade num:' + str(trade_df['trade'].abs().sum()))
t3 = time()


####################绩效报告#######################
# 转换成日频结果
daily_df = pd.DataFrame(trade_df['pnl'].resample('D').sum())
daily_df['fee'] = trade_df['fee'].resample('D').sum()
daily_df['trade_num'] = trade_df['trade'].abs().resample('D').sum()
daily_df = daily_df.loc[date_list,:]
daily_df['balance'] = daily_df['pnl'].cumsum() +balance
daily_df['rtn'] = daily_df['pnl'] / daily_df['balance']
daily_df['nav'] = daily_df['rtn'].cumsum() + 1
# 绩效指标
dailyPnl = daily_df['rtn']
tradeDays = dailyPnl.shape[0]
totalRtn = dailyPnl.sum()
yearlyRtn = totalRtn * 240 / tradeDays
yearlyVol = dailyPnl.std() * np.sqrt(240)
nav = dailyPnl.cumsum() + 1
tmpnav = np.maximum.accumulate(nav) - nav
idx_e = tmpnav.idxmax()
idx_s = nav[:idx_e].idxmax()
maxDD = -(nav[idx_e] - nav[idx_s])
maxDD_length = len(nav[idx_s:idx_e])
maxDD_start = idx_s
maxDD_end = idx_e
sharp = (yearlyRtn - 0.03) / yearlyVol
calmar = yearlyRtn / maxDD
report_dict = {
'tradeDays':tradeDays,
'totalRtn':totalRtn,
'yearlyRtn':yearlyRtn,
'yearlyVol':yearlyVol,
'maxDD':maxDD,
'sharp':sharp,
'calmar':calmar
}
report = pd.DataFrame(report_dict,index=[0])
t4 = time()

print(f'准备数据——耗时：%.2f s \n策略逻辑——耗时：%.2f s\n交易清算——耗时：%.2f s\n绩效报告——耗时：%.2f s\n总耗时：%.2fs \n ' %(
    t1-t0, t2-t1,t3-t2,t4-t3, t4-t0))



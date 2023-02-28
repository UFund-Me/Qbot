## 🔗 ref https://mp.weixin.qq.com/s/MiG09Z3jDLFQhcncJ9UBOw

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def calcRSI(data, P=14):
  # Calculate gains and losses
  data['diff_close'] = data['Close'] - data['Close'].shift(1)
  data['gain'] = np.where(data['diff_close']>0,
    data['diff_close'], 0)
  data['loss'] = np.where(data['diff_close']<0,
    np.abs(data['diff_close']), 0)
  
  # Get initial values
  data[['init_avg_gain', 'init_avg_loss']] = data[
    ['gain', 'loss']].rolling(P).mean()
  # Calculate smoothed avg gains and losses for all t > P
  avg_gain = np.zeros(len(data))
  avg_loss = np.zeros(len(data))
  
  for i, _row in enumerate(data.iterrows()):
    row = _row[1]
    if i < P - 1:
      last_row = row.copy()
      continue
    elif i == P-1:
      avg_gain[i] += row['init_avg_gain']
      avg_loss[i] += row['init_avg_loss']
    else:
      avg_gain[i] += ((P - 1) * avg_gain[i-1] + row['gain']) / P
      avg_loss[i] += ((P - 1) * avg_loss[i-1] + row['loss']) / P
    
    last_row = row.copy()
  
  data['avg_gain'] = avg_gain
  data['avg_loss'] = avg_loss
  # Calculate RS and RSI
  data['RS'] = data['avg_gain'] / data['avg_loss']
  data['RSI'] = 100 - 100 / (1 + data['RS'])
  return data

def calcStochOscillator(data, N=14):
  data['low_N'] = data['RSI'].rolling(N).min()
  data['high_N'] = data['RSI'].rolling(N).max()
  data['StochRSI'] = 100 * (data['RSI'] - data['low_N']) / (data['high_N'] - data['low_N'])
  return data

def calcStochRSI(data, P=14, N=14):
  data = calcRSI(data, P)
  data = calcStochOscillator(data, N)
  return data

def calcReturns(df):
  # Helper function to avoid repeating too much code
  df['returns'] = df['Close'] / df['Close'].shift(1)
  df['log_returns'] = np.log(df['returns'])
  df['strat_returns'] = df['position'].shift(1) * df['returns']
  df['strat_log_returns'] = df['position'].shift(1) * df['log_returns']
  df['cum_returns'] = np.exp(df['log_returns'].cumsum()) - 1
  df['strat_cum_returns'] = np.exp(df['strat_log_returns'].cumsum()) / - 1
  df['peak'] = df['cum_returns'].cummax()
  df['strat_peak'] = df['strat_cum_returns'].cummax()
  return df


def StochRSIReversionStrategy(data, P=14, N=14, short_level=80,
  buy_level=20, shorts=True):
  '''
  Buys when the StochRSI is oversold and sells when it's
  overbought
  '''
  df = calcStochRSI(data, P, N)
  df['position'] = np.nan
  df['position'] = np.where(df['StochRSI']<buy_level, 1,
    df['position'])
  if shorts:
    df['position'] = np.where(df['StochRSI']>short_level, -1, 
      df['position'])
  else:
    df['position'] = np.where(df['StochRSI']>short_level, 0,   
      df['position'])
  
  df['position'] = df['position'].ffill().fillna(0)
  return calcReturns(df)


table = pd.read_html(
  'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
syms = df['Symbol']

# Sample symbols
ticker = np.random.choice(syms.values)
print(f"Ticker Symbol: {ticker}")
start = '2000-01-01'
end = '2020-12-31'

# Get Data
yfObj = yf.Ticker(ticker)
data = yfObj.history(start=start, end=end)
data.drop(['Open', 'High', 'Low', 'Volume', 'Dividends',
  'Stock Splits'], inplace=True, axis=1)

# Run test
df_rev = StochRSIReversionStrategy(data.copy())

# Plot results
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
fig, ax = plt.subplots(2, figsize=(12, 8))

ax[0].plot(df_rev['strat_cum_returns']*100, label='Mean Reversion')
ax[0].plot(df_rev['cum_returns']*100, label='Buy and Hold')
ax[0].set_ylabel('Returns (%)')
ax[0].set_title('Cumulative Returns for Mean Reversion and' +
    f' Buy and Hold Strategies for {ticker}')
ax[0].legend(bbox_to_anchor=[1, 0.6])

ax[1].plot(df_rev['StochRSI'], label='StochRSI', linewidth=0.5)
ax[1].plot(df_rev['RSI'], label='RSI', linewidth=1)
ax[1].axhline(80, label='Over Bought', color=colors[1], linestyle=':')
ax[1].axhline(20, label='Over Sold', color=colors[2], linestyle=':')
ax[1].axhline(50, label='Centerline', color='k', linestyle=':')
ax[1].set_ylabel('Stochastic RSI')
ax[1].set_xlabel('Date')
ax[1].set_title(f'Stochastic RSI for {ticker}')
ax[1].legend(bbox_to_anchor=[1, 0.75])

plt.tight_layout()
plt.show()

# Get trades
diff = df_rev['position'].diff().dropna()
trade_idx = diff.index[np.where(diff!=0)]

fig, ax = plt.subplots(1, figsize=(12, 8))
ax.plot(df_rev['Close'], linewidth=1, label=f'{ticker}')
ax.scatter(trade_idx, df_rev.loc[trade_idx]['Close'], c=colors[1],
  marker='^', label='Trade')
ax.set_ylabel('Price')
ax.set_title(f'{ticker} Price Chart and Trades for' +
  'StochRSI Mean Reversion Strategy')
ax.legend()
plt.show()


def getStratStats(log_returns: pd.Series, 
  risk_free_rate: float = 0.02):
  stats = {}

  # Total Returns
  stats['tot_returns'] = np.exp(log_returns.sum()) - 1
 
 # Mean Annual Returns
  stats['annual_returns'] = np.exp(log_returns.mean() * 252) - 1
 
  # Annual Volatility
  stats['annual_volatility'] = log_returns.std() * np.sqrt(252)
  
  # Sortino Ratio
  annualized_downside = log_returns.loc[log_returns<0].std() * np.sqrt(252)
  stats['sortino_ratio'] = (stats['annual_returns'] - 
    risk_free_rate) / annualized_downside

  # Sharpe Ratio
  stats['sharpe_ratio'] = (stats['annual_returns'] - 
    risk_free_rate) / stats['annual_volatility']

  # Max Drawdown
  cum_returns = log_returns.cumsum() - 1
  peak = cum_returns.cummax()
  drawdown = peak - cum_returns
  stats['max_drawdown'] = drawdown.max()

  # Max Drawdown Duration
  strat_dd = drawdown[drawdown==0]
  strat_dd_diff = strat_dd.index[1:] - strat_dd.index[:-1]
  strat_dd_days = strat_dd_diff.map(lambda x: x.days).values
  strat_dd_days = np.hstack([strat_dd_days,
    (drawdown.index[-1] - strat_dd.index[-1]).days])
  stats['max_drawdown_duration'] = strat_dd_days.max()

  return stats

rev_stats = getStratStats(df_rev['strat_log_returns'])
bh_stats = getStratStats(df_rev['log_returns'])

pd.concat([
  pd.DataFrame(rev_stats, index=['Mean Reversion']),
  pd.DataFrame(bh_stats, index=['Buy and Hold'])])

print(pd)
## https://mp.weixin.qq.com/s/tvYMwNIqA9ZNKb88PiSIew

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
from pandas_datareader import data

#download Apple price data into DataFrame
apple = data.DataReader('AAPL', 'yahoo', start='1/1/2000')

#calculate the compound annual growth rate (CAGR) which 
#will give us our mean return input (mu) 
days = (apple.index[-1] - apple.index[0]).days
cagr = ((((apple['Adj Close'][-1]) / apple['Adj Close'][1])) ** (365.0/days)) - 1
print ('CAGR =',str(round(cagr,4)*100)+"%")
mu = cagr

#create a series of percentage returns and calculate 
#the annual volatility of returns
apple['Returns'] = apple['Adj Close'].pct_change()
vol = apple['Returns'].std() * sqrt(252)
print ("Annual Volatility =",str(round(vol,4)*100)+"%")

# blog https://blog.csdn.net/qq_44176343/article/details/109903512
import tushare as ts
import matplotlib.pyplot as plt
import seaborn as sns

# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
# pip install --upgrade mplfinance
import mpl_finance as mpf 

token = "6f747880359ef14fe2fd5fc0c2c08a4e09a47e7ac161d643ae7036c0"
pro = ts.pro_api(token)
df = ts.get_k_data('000002','2019-06-01','2019-09-30')

# 导入调整日期格式涉及的两个库
from matplotlib.pylab import date2num
import datetime
 
# 将Tushare库中获取到的日期数据转换成candlestick_ochl()函数可读取的格式
def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time
 
# 将DataFrame转换为二维数组，并利用date_to_num()函数转换日期格式
df_arr = df.values  #将DataFrame格式的数据转换为二维数组
# df_arr
df_arr[:,0] = date_to_num(df_arr[:,0])  #将二维数组中的日期转换成数字格式

df['MA5'] = df['close'].rolling(5).mean()
df['MA10'] = df['close'].rolling(10).mean()

fig,axes = plt.subplots(2,1,sharex=True,figsize=(15,8))
ax1,ax2 = axes.flatten()
 
# 绘制K线图和均线图
mpf.candlestick_ochl(ax1,df_arr,width=0.6,colorup='r',colordown='g',alpha=1.0)
ax1.plot(df_arr[:,0],df['MA5'])
ax1.plot(df_arr[:,0],df['MA10'])
 
ax1.grid()
ax1.xaxis_date()
ax1.set_title('万科A',fontsize=16)
ax1.set_ylabel('价格',fontsize=16)
 
# 绘制每日成交量图
ax2.bar(df_arr[:,0],df_arr[:,5])
ax2.set_xlabel('日期',fontsize=16)
ax2.set_ylabel('成交量',fontsize=16)
ax1.grid()
ax1.xaxis_date()

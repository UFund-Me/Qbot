import tushare as ts
from datetime import datetime
import matplotlib.pyplot as plt
import mpl_finance as mpf
import datetime  #导入日期格式涉及的两个库
import seaborn as sns  #引入图表美化库

df = ts.get_k_data('000002',start ='2009-01-01',end='2019-01-01')

#要注意细节，调整日期格式，让横坐标的显示效果更佳清洗，美观
# df['date'] = df['date'].apply(lambda x:datetime.strptime(x,'%Y-%m-%d'))
# plt.plot(df['date'],df['close'])
# plt.show()

# sns.set()#激活
# df = ts.get_k_data('000002','2019-06-01','2019-09-30')
# df.head()

def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

df_arr = df.values  #将DataFrame中数据转换成二维数组
df_arr[:,0] = date_to_num(df_arr[:,0])#  将二维数组中日期转换成数字格式


fig,ax = plt.subplots(figsize = (15,6))
mpf.candlestick_ochl(ax,df_arr,width = 0.6,colorup = 'r',colordown = 'g',alpha = 1.0)
plt.grid(True)#绘制网格线
ax.xaxis_date()#设置x轴的刻度线格式为常规日期格式

# df['MA5'] = df['close'].rolling(5).mean()
# df['MA10'] = df['close'].rolling(10).mean()

# plt.rcParams['font.sans-serif'] = ['SimHei'] #设置正常中文显示
# fig,ax = plt.subplots(figsize = (15,6))
# mpf.candlestick_ochl(ax,df_arr,width = 0.6,colorup = "r",colordown = 'g',alpha = 1.0) #绘制K直线
# plt.plot(df_arr[:,0],df["MA5"])
# plt.plot(df_arr[:,0],df['MA10'])
# plt.grid(True)  #绘制网格线
# plt.title('万科A')#标题
# plt.xlabel('日期')#X轴
# plt.ylabel('价格')#y轴
# ax.xaxis_date()


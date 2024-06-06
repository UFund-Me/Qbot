import numpy as np
from sklearn.preprocessing import MinMaxScaler
import torch
from torch.autograd import Variable
from torch.utils.data import TensorDataset
from date_time_func import *
import re


# 加载tick数据文件（parquet)
def get_future_tick(code='RB2305', date='20230206'):
    fname = f'data_file\\{code}_{date}.parquet'
    df = pd.read_parquet(fname)
    return df


# 将tick数据转换成指定频率的K线数据
def compute_future_tick_resample(code='RB2305', date='20230206', freq='10s', win=30):
    tick_df = get_future_tick(code, date)
    tick_resample = pd.DataFrame(tick_df['price'].resample(freq, label='right').last())
    tick_resample['Close'] = tick_df['price'].resample(freq, label='right').last()
    tick_resample['High'] = tick_df['price'].resample(freq, label='right').max()
    tick_resample['Low'] = tick_df['price'].resample(freq, label='right').min()
    tick_resample['Open'] = tick_df['price'].resample(freq, label='right').first()
    tick_resample['Volume'] = tick_df['vol'].resample(freq, label='right').sum()
    tick_resample['Amount'] = tick_df['amt'].resample(freq, label='right').sum()
    tick_resample['OI'] = tick_df['oi'].resample(freq, label='right').last()

    time_list = get_future_time_list(future_type=re.findall(r'[A-Z]+', code)[0], date=date, freq=freq)
    tick_resample = tick_resample.loc[time_list, :]
    tick_resample['rtn'] = tick_resample['price'].apply(np.log).diff().fillna(0)
    tick_resample['rtn_fut'] = 0
    tick_resample['rtn_fut'].iloc[:-win] = tick_resample['rtn'].rolling(window=win).sum().fillna(0).tolist()[win:]

    tick_resample['Bid'] = tick_df['bp01'].resample(freq, label='right').mean()
    tick_resample['Ask'] = tick_df['sp01'].resample(freq, label='right').mean()
    # tick_resample['price_ma'] = tick_resample['price'].rolling(window=win).mean()
    return tick_resample


# 提取数据API，输入代码，起止时间，频率
def get_future_tick_resample(code='RB2305', start_date='20230206', end_date='20230207', freq='10s'):
    date_list = get_trade_date_list(start_date, end_date)
    date_list = [str(x).replace('-','')[:8] for x in date_list]
    bar_df = pd.DataFrame()
    for date in date_list:
        df = compute_future_tick_resample(code, date, freq)
        bar_df = pd.concat([bar_df, df])
    return  bar_df



# 数据标准化
def normalization(data, label, normal_flag):
    mm_x=MinMaxScaler()
    mm_y=MinMaxScaler()
    data=data.values
    label=label.values
    label = label.reshape(-1,1)
    if normal_flag == 1:
        data=mm_x.fit_transform(data) # 对数据和标签进行标准化
        label=mm_y.fit_transform(label)
    return data,label,mm_y

# 时间向量转换
def split_windows(data,label, seq_length):
    x=[]
    y=[]
    for i in range(len(data)-seq_length-1):
        _x=data[i:(i+seq_length),:]
        _y=label[i+seq_length,0]
        x.append(_x)
        y.append(_y)
    x,y=np.array(x),np.array(y)
    # print('x.shape,y.shape=\n',x.shape,y.shape)
    return x,y

# 训练集、测试集切分
def split_data(x,y,split_ratio):

    train_size=int(len(y)*split_ratio)
    test_size=len(y)-train_size

    x_data=Variable(torch.Tensor(np.array(x)))
    y_data=Variable(torch.Tensor(np.array(y)))

    x_train=Variable(torch.Tensor(np.array(x[0:train_size])))
    y_train=Variable(torch.Tensor(np.array(y[0:train_size])))
    y_test=Variable(torch.Tensor(np.array(y[train_size:len(y)])))
    x_test=Variable(torch.Tensor(np.array(x[train_size:len(x)])))
    return x_data,y_data,x_train,y_train,x_test,y_test

# 数据装入DataLoader
def data_generator(x_train,y_train,x_test,y_test,n_iters,batch_size):
    num_epochs=n_iters/(len(x_train)/batch_size) # n_iters代表一次迭代
    num_epochs=int(num_epochs)
    train_dataset=TensorDataset(x_train,y_train)
    test_dataset=TensorDataset(x_test,y_test)
    train_loader=torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=False,drop_last=True) # 加载数据集,使数据集可迭代
    test_loader=torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=False,drop_last=True)
    return train_loader,test_loader,num_epochs

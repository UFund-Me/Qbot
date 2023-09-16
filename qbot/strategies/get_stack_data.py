'''
Author: Charmve yidazhang1@gmail.com
Date: 2023-03-18 18:09:25
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-03-18 18:09:26
FilePath: /Qbot/qbot/strategies/get_stack_data.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
'''

#使用tushare旧版获取数据
import tushare as ts
def get_from_tushare(code,adj='hfq',start='2010-01-01',end='2021-11-05'):
    df=ts.get_k_data(code,autype=adj,start=start,end=end)
    df.index=pd.to_datetime(df.date)
    #原数据已默认按日期进行了排序
    return df
 
#使用tushare pro获取数据
import tushare as ts
token='输入你自己的token'
pro=ts.pro_api(token)
ts.set_token(token)
def get_from_tushare_pro(code,adj='hfq',start='2010-01-01',end='2021-11-05'):
    #code:输入数字字符串，如‘300002’
    #start和end输入'年-月-日'需转为'年月日'格式
    if code.startswith('6'):
        code=code+'.SH'
    else:
        code=code+'.SZ'
    start=''.join(start.split('-'))
    end=''.join(end.split('-'))
    df=ts.pro_bar(ts_code=code,adj=adj,start_date=start,end_date=end)
    #原数据是倒序的，所以将时间设置为索引，根据索引重新排序
    df.index=pd.to_datetime(df.trade_date)
    df=df.sort_index()
    return df
 
#使用akshare获取数据,其数据源来自新浪，与tushare旧版本相似
import akshare as ak
def get_from_akshare(code,adj='hfq',start='2010-01-01',end='2021-11-05'):
    if code.startswith('6'):
        code='sh'+code
    else:
        code='sz'+code
    start=''.join(start.split('-'))
    end=''.join(end.split('-'))
    df = ak.stock_zh_a_daily(symbol=code, start_date=start, end_date=end, adjust=adj)
    return df
 
#使用baostock获取数据
import baostock as bs
def get_from_baostock(code,adj='hfq',start='2010-01-01',end='2021-11-05'):
    if code.startswith('6'):
        code='sh.'+code
    else:
        code='sz.'+code
    #转换复权为数字
    if adj=='hfq':
        adj='1'
    elif adj=='qfq':
        adj='2'
    else:
        adj='3'
    #必须登陆和登出系统
    bs.login() #登陆系统
    rs = bs.query_history_k_data_plus(code,
       fields="date,code,open,high,low,close,volume",
       start_date=start, end_date=end,
       frequency="d", adjustflag=adj)
    #adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    #将数据转为dataframe格式
    df = pd.DataFrame(data_list, columns=rs.fields)
    df.index=pd.to_datetime(df.date)
    bs.logout() #登出系统 
    return df
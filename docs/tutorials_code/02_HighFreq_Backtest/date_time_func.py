import pandas as pd
import os

def init_calender():
    tdate_df = pd.read_csv('calender.csv')
    tdate_df.index = tdate_df.iloc[:,0].apply(lambda x: str(pd.Timestamp(str(x)))[:10])
    tdate_df['cal_date'] = tdate_df.index
    tdate_df.to_csv('calender.csv')

def get_trade_date_list(sd='20230101', ed='20230301'):
    sd = pd.Timestamp(sd)
    ed = pd.Timestamp(ed)
    path = os.path.abspath(os.path.dirname(__file__))
    tdate_df = pd.read_csv(os.path.join(path,'calender.csv'), index_col=0)
    tdate_df.index = pd.DatetimeIndex(tdate_df.index)
    select_df = tdate_df.loc[sd:ed,:]
    select_list = select_df['cal_date'].tolist()
    a = 1
    return select_list

def get_next_trade_date(date='20230206', step=-1):
    date = pd.Timestamp(date)
    path = os.path.abspath(os.path.dirname(__file__))
    tdate_df = pd.read_csv(os.path.join(path,'calender.csv'), index_col=0)
    tdate_df.index = pd.DatetimeIndex(tdate_df.index)
    if step < 0:
        step_date = tdate_df.loc[tdate_df['cal_date'] < str(date)[:10],'cal_date'].iloc[step]
    else:
        step_date = tdate_df.loc[tdate_df['cal_date'] > str(date)[:10],'cal_date'].iloc[step]
    return step_date

time_mode = {
    'mode1': {'night':['21:00:00','23:00:00'],
              'day':[['09:00:00','10:15:00'],['10:30:00','11:30:00'],['13:30:00','15:00:00']]},
}

future_mode_map = {
    'RB':'mode1'
}

def get_future_time_list(future_type='RB', date='2023-02-06', freq='10s'):
    
    # mode_dict = time_mode[future_mode_map[future_type]]
    mode_dict = time_mode['mode1']
    pre_date = get_next_trade_date(date,-1)
    total_time_list = []
    if 'night' in mode_dict.keys():
        n_mode = mode_dict['night']
        total_time_list = list(pd.date_range(pre_date+' '+n_mode[0],pre_date+' '+n_mode[1], freq=freq, closed='right'))

    d_mode = mode_dict['day']
    for dm in d_mode:
        total_time_list += list(pd.date_range(date+' '+dm[0], date+' '+dm[1], freq=freq, closed='right'))


    return total_time_list




if __name__ == '__main__':
    get_future_time_list()




import tushare as ts

mytoken = '565ee6d69fb85cb0bc7fdfc8dea4b8ce1f18366f30e8d23a253bb9cf'
ts.set_token(mytoken)
pro = ts.pro_api()


def get_daily(ts_code, start_date, end_date):
    # get stock daily price and other info from start_date to end_date 
    try:
        df = pro.daily(ts_code=ts_code,
                       start_date=start_date,
                       end_date=end_date)
    except Exception as e:
        print('Retry, We get error:', e)
        df = get_daily()
    return df


def get_stock_basic():
    # get all stock basic info
    try:
        df = pro.stock_basic(
            exchange='',
            list_status='L',
            fields='ts_code,symbol,name,area,industry,list_date')
    except Exception as e:
        print('Retry, We get error:', e)
        df = get_stock_basic()
    return df


def get_daily_basic(trade_date):
    # get all stock daily_basic info
    try:
        df = pro.daily_basic(
            ts_code='',
            trade_date=trade_date,
            fields='ts_code,tradtutorials_codee_date,turnover_rate,volume_ratio,pe,pb')
    except Exception as e:
        print('Retry, We get error:', e)
        df = get_daily_basic(trade_date)
    return df


def get_income(code, start_date, end_date):
    try:
        income = pro.income(ts_code=code,
                            start_date=start_date,
                            end_date=end_date,
                            fields='ts_code,basic_eps,diluted_eps')
    except Exception as e:
        print('Retry, We get error:', e)
        income = get_income(code, start_date, end_date)
    return income

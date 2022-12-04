import os

import pandas as pd


def load_data(codes, start_time="20100101", end_time="20211231"):
    dfs = []
    for code in codes:
        df = load_from_file(code)
        df.dropna(inplace=True)
        dfs.append(df)
    df_all = pd.concat(dfs, axis=0)
    df_all.sort_index(inplace=True)
    df_all = df_all.loc[start_time:end_time]
    return df_all


def load_from_file(code):
    path = os.path.dirname(__file__)
    filename = "{}/{}.csv".format(os.path.dirname(path) + "/data/indexes", code)
    # print("stack data:" + filename)
    if os.path.exists(filename):
        df = pd.read_csv(filename, index_col=[0])
        # print(df.head())
        df.rename(
            columns={"trade_date": "date", "ts_code": "code", "vol": "volume"},
            inplace=True,
        )
        df["date"] = df["date"].apply(lambda x: str(x))
        df = df[["code", "open", "high", "low", "close", "date", "volume"]]
        # df = df[['open', 'high', 'low', 'close', 'date', 'volume']]
        df.index = df["date"]
        df.sort_index(ascending=True, inplace=True)
        df["rate"] = df["close"].pct_change()
    else:
        print("load_from_file error")
        return None
    return df

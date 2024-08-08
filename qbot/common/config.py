"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-05-14 18:18:42
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2024-03-29 13:44:26
FilePath: /qbot_pro/qbot/engine/config.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description:

Copyright (c) 2023 by Charmve, All Rights Reserved.
Licensed under the MIT License.
"""

from pathlib import Path

QBOT_TOP_DIR = Path(__file__).parent.parent.parent

DATA_DIR = Path(__file__).parent.parent.parent.joinpath("data")
RESULT_DIR = Path(__file__).parent.parent.parent.joinpath("results")
ASSERTS_DIR = Path(__file__).parent.parent.joinpath("asserts")
DOCS_DIR = Path(__file__).parent.parent.parent.joinpath("docs")
ENGINE_DIR = Path(__file__).parent.parent.parent.joinpath("qbot/engine")

DATA_DIR_HDF5 = DATA_DIR.joinpath("hdf5")
DATA_DIR_CSV = DATA_DIR.joinpath("stocks")
FUTURES_DATA_DIR = DATA_DIR.joinpath("futures")
FUNDS_DATA_DIR = DATA_DIR.joinpath("funds")
BTC_DATA_DIR = DATA_DIR.joinpath("btc")
OPTIONS_DATA_DIR = DATA_DIR.joinpath("options")

MULTI_FACTS_DIR = DATA_DIR.joinpath("multi-facts")
QLIB_MLRUNS_DIR = DATA_DIR.joinpath("qlib_mlruns")
QLIB_DATA_DIR = DATA_DIR.joinpath("qlib_data")
DATA_DIR_HDF5_ALL = DATA_DIR_HDF5.joinpath("all.h5")
DATA_DIR_HDF5_CACHE = DATA_DIR_HDF5.joinpath("cache.h5")

DATA_DIR_HDF5_BKT_RESULTS = RESULT_DIR.joinpath("hdf5")
BKT_RESULT_DIR = RESULT_DIR.joinpath("bkt_result")
INDICAT_RESULT_DIR = RESULT_DIR.joinpath("indicators")
BACKTEST_RESULT_DIR = RESULT_DIR.joinpath("bk_result")

RESEARCH_REPORTS = DOCS_DIR.joinpath("research_reports")
NOTEBOOK_DIR = DOCS_DIR.joinpath("notebook")

STOCK_LIST_CSV = DATA_DIR.joinpath("stock_code.csv")
FUTURES_LIST_CSV = DATA_DIR.joinpath("futures_code.csv")
OPTIONS_LIST_CSV = DATA_DIR.joinpath("options_code.csv")

TOKENS_FILE = ENGINE_DIR.joinpath("tokens.json")

STOCK_REAL_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/stocks/account.json")
FUTURES_REAL_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/futures/account.json")
OPTIONS_REAL_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/options/account.json")
BTC_REAL_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/btc/account.json")
FUNDS_REAL_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/funds/account.json")

STOCK_SIM_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/stocks/sim_account.json")
FUTURES_SIM_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/futures/sim_account.json")
OPTIONS_SIM_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/options/sim_account.json")
BTC_SIM_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/btc/sim_account.json")
FUNDS_SIM_ACCOUNT = ENGINE_DIR.joinpath("trade/engine_apis/funds/sim_account.json")

dirs = [
    DATA_DIR,
    RESULT_DIR,
    DATA_DIR_CSV,
    BKT_RESULT_DIR,
    INDICAT_RESULT_DIR,
    MULTI_FACTS_DIR,
    QLIB_MLRUNS_DIR,
    QLIB_DATA_DIR,
    DATA_DIR_HDF5_BKT_RESULTS,
    RESEARCH_REPORTS,
    NOTEBOOK_DIR,
]
for dir in dirs:
    dir.mkdir(exist_ok=True, parents=True)

import pickle

import pandas as pd
import qlib
from qlib.config import REG_CN
from qlib.contrib.evaluate import backtest_daily, risk_analysis
from qlib.contrib.strategy import TopkDropoutStrategy

if __name__ == "__main__":
    # init qlib
    qlib.init(provider_uri="../data/cn_data", region=REG_CN)

    with open(
        "mlruns/3/ee9de2cb147348c58cfe2dd0bf06f5f6/artifacts/pred.pkl", "rb"
    ) as f:
        pred_score = pickle.load(f)

    CSI300_BENCH = "SH000300"
    STRATEGY_CONFIG = {
        "topk": 50,
        "n_drop": 5,
        # pred_score, pd.Series
        "signal": pred_score,
    }

    strategy_obj = TopkDropoutStrategy(**STRATEGY_CONFIG)
    report_normal, positions_normal = backtest_daily(
        start_time="2017-01-01", end_time="2020-08-01", strategy=strategy_obj
    )
    analysis = dict()
    analysis["excess_return_without_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"], freq="day"
    )
    analysis["excess_return_with_cost"] = risk_analysis(
        report_normal["return"] - report_normal["bench"] - report_normal["cost"],
        freq="day",
    )

    analysis_df = pd.concat(analysis)  # type: pd.DataFrame
    print(analysis_df)

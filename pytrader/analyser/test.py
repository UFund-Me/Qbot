import pandas as pd
import qlib
from qlib.config import REG_CN
from qlib.contrib.report import analysis_model, analysis_position
from qlib.workflow import R

qlib.init(provider_uri="../data/cn_data", region=REG_CN)

recorder = R.get_recorder(
    recorder_id="cfb1dc0830294571a67fc6a862e1cc1e", experiment_name="backtest_analysis"
)
# recorder = R.get_recorder(recorder_id=ba_rid, experiment_name="backtest_analysis")
print(recorder)
pred_df = recorder.load_object("pred.pkl")
pred_df_dates = pred_df.index.get_level_values(level="datetime")
report_normal_df = recorder.load_object("portfolio_analysis/report_normal_1day.pkl")
positions = recorder.load_object("portfolio_analysis/positions_normal_1day.pkl")
analysis_df = recorder.load_object("portfolio_analysis/port_analysis_1day.pkl")

label_df = dataset.prepare("test", col_set="lable")
label_df.columns = ["lable"]

pred_label = pd.connect([label_df, pred_df], axis=1, sort=True).reindex(label_df.index)
analysis_position.score_ic_graph(pred_label)

analysis_model.model_performance_graph(pred_label)

report_graph = analysis_position.report_graph(report_normal_df, show_notebook=False)
for fig in report_graph:
    fig.show()

risk_analysis_graph = analysis_position.risk_analysis_graph(
    analysis_df, report_normal_df, show_notebook=False
)
for fig in risk_analysis_graph:
    fig.show()

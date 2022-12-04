import qlib
from qlib.config import REG_CN
from qlib.data.dataset.loader import QlibDataLoader

if __name__ == "__main__":
    MACD_EXP = "(EMA($close, 12) - EMA($close, 26))/$close - EMA((EMA($close, 12) - EMA($close, 26))/$close, 9)/$close"
    fields = [MACD_EXP, "$close"]  # MACD
    names = ["MACD", "CLOSE"]
    labels = [
        "Ref($close, -2)/Ref($close, -1) - 1",
        "$close/Ref($close,5) - 1",
    ]  # label
    label_names = ["LABEL", "MOMENTUM5"]

    qlib.init(provider_uri="../data/cn_data", region=REG_CN)

    data_loader_config = {"feature": (fields, names), "label": (labels, label_names)}

    data_loader = QlibDataLoader(config=data_loader_config)
    df = data_loader.load(
        instruments="all", start_time="2010-01-01", end_time="2017-12-31"
    )

    print(df)

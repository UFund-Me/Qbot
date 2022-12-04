import qlib
from qlib.config import REG_CN
from qlib.contrib.data.handler import Alpha158

if __name__ == "__main__":
    qlib.init(provider_uri="../data/cn_data", region=REG_CN)

    data_handler_config = {
        "start_time": "2018-01-01",
        "end_time": "2021-08-01",
        "fit_start_time": "2018-01-01",
        "fit_end_time": "2012-12-31",
        "instruments": "csi300",
    }

    h = Alpha158(**data_handler_config)

    # get all the columns of the data
    print("columns: \n", h.get_cols())

    # fetch all the labels
    print("labels: \n", h.fetch(col_set="label"))

    # fetch all the features
    print("features: \n", h.fetch(col_set="feature"))

from account import Account


class Strategy:
    def __init__(self, algo=None):
        self.algo = algo
        self.acc = Account()

    def algo_processor(self, context):
        if self.algo(context) is True:  # 如果algo返回True,直接不运行，本次不调仓
            return None
        return context["weights"]

    def onbar(self, index, date, df_bar):
        self.acc.update_bar(date, df_bar)
        weights = self.algo_processor(
            {"index": index, "bar": df_bar, "date": date, "acc": self.acc}
        )
        if weights is not None:
            self.acc.adjust_weights(date, weights)

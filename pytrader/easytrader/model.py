from dataclasses import dataclass


@dataclass
class Balance:
    """
    资产
    """

    # 总资产
    asset_balance: float

    current_balance: float

    # 可用
    enable_balance: float

    frozen_balance: float

    # 市值
    market_value: float

    # 币种
    money_type: str

    pre_interest: float = 0

    def update(self, market_value, current_balance):
        self.market_value = market_value
        self.current_balance = current_balance
        self.asset_balance = self.current_balance + self.market_value

    def update_total(self):
        self.asset_balance = self.current_balance + self.market_value

@dataclass
class Position:
    """
    持仓
    """
    current_amount: int
    enable_amount: int
    income_balance: int
    cost_price: float
    last_price: float
    market_value: float
    position_str: str
    stock_code: str
    stock_name: str

    def update(self, last_price: float):
        self.last_price = last_price
        self.market_value = self.current_amount * last_price


@dataclass
class Entrust:
    """
    历史委托
    """
    entrust_no: str
    # 买卖类别
    bs_type: str
    entrust_amount: int
    entrust_price: float
    report_time: str
    entrust_status: str
    stock_code: str
    stock_name: str
    # 费用
    cost: float


@dataclass
class PerTrade:
    """
    交易费用
    """
    # 买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    close_tax=0.001
    buy_cost = 0.003
    sell_cost = 0.004
    min_cost = 5


@dataclass
class Deal:
    """
    当日成交
    """
    deal_no: str
    entrust_no: str
    # 买卖类别
    bs_type: str
    entrust_amount: int
    deal_amount: int
    deal_price: float
    entrust_price: float
    # HHmmss
    deal_time: str
    stock_code: str
    stock_name: str


@dataclass
class IPOQuota:
    """IPO配额"""
    account_code: str
    market: str
    quota: int


@dataclass
class IPO:
    # {
    #     "Market": "SA",
    #     "Sgrq": "20210928",
    #     "Zqdm": "301080",
    #     "Zqmc": "百普赛斯",
    #     "Sgdm": "301080",
    #     "Fxzs": "2000",
    #     "Wsfxs": "2000",
    #     "Fxj": "112.50",
    #     "Yc_Fxj": "",
    #     "Sgsx": "20000.00",
    #     "Yc_Sgsx": "2",
    #     "Sgzjsx": "",
    #     "Yc_Sgzjsx": "",
    #     "Ksgsx": "20000",
    #     "SgState": "-1",
    #     "Min_Step": "500",
    #     "CDR_Flag": "0",
    #     "YL_Flag": "Y",
    #     "TPQCY_FLag": "N",
    #     "Cybbz": "1",
    #     "SFZCZ": "Y",
    #     "JYXYJG": "N",
    #     "APPLYPRICE": ""
    # }
    """
    新股申购
    """
    market: str
    stock_code: float
    stock_name: float

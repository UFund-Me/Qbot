__version__ = "0.11.7"
__author__ = "refraction-ray"
__name__ = "xalpha"

import xalpha.policy
import xalpha.remain
import xalpha.misc
import xalpha.exceptions
from xalpha.evaluate import evaluate
from xalpha.info import (
    fundinfo,
    indexinfo,
    cashinfo,
    mfundinfo,
    FundInfo,
    IndexInfo,
    CashInfo,
    MFundInfo,
    FundReport,
    get_fund_holdings,
)
from xalpha.multiple import mul, mulfix, imul, Mul, MulFix, IMul
from xalpha.realtime import rfundinfo, review  # deprecated
from xalpha.record import record, irecord, Record, IRecord
from xalpha.trade import trade, itrade, Trade, ITrade
from xalpha.universal import (
    get_daily,
    get_rt,
    get_bar,
    set_backend,
    set_handler,
    vinfo,
    VInfo,
)
from xalpha.provider import show_providers, set_proxy
from xalpha.toolbox import (
    PEBHistory,
    IndexPEBHistory,
    FundPEBHistory,
    SWPEBHistory,
    StockPEBHistory,
    TEBHistory,
    Compare,
    OverPriced,
    QDIIPredict,
    RTPredict,
    CBCalculator,
    set_holdings,
    set_display,
)
import xalpha.backtest

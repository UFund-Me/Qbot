"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-05-20 16:37:34
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-09-20 10:16:19
FilePath: /Qbot/gui/panels/panel_backtest.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description: 

Copyright (c) 2023 by Charmve, All Rights Reserved. 
Licensed under the MIT License.
"""
import wx

from qbot.gui.config import DATA_DIR_BKT_RESULT
from qbot.gui.widgets.widget_web import WebPanel
from qbot.common.file_utils import extract_content
from qbot.common.logging.logger import LOGGER as logger
from qbot.common.macros import strategy_choices

# https://zhuanlan.zhihu.com/p/376248349
def OnBkt(event):
    wx.MessageBox("ok")


class PanelBacktest(wx.Panel):
    def __init__(self, parent=None, id=-1, displaySize=(1600, 900)):
        super(PanelBacktest, self).__init__(parent)

        self.backtest_opts = {
            "start_time": "20100101",
            "end_time": "20211231",
            "benchmark": "000300.SH",
            "code": "399006.SZ",
            "select_strategy": "单因子-相对强弱指数RSI",
        }

        self.backtest_config = {
            "limit_threshold": 0.095,
            "init_cash": 10000,
            "deal_price": "close",
            "open_cost": 0.0005,
            "slippage": 0.1,
            "stake": 100,  # 每笔交易量
            "commission": 0.0005,
            "stamp_duty": 0.001,
            "close_cost": 0.0015,
            "min_cost": 5,
        }

        # M1 与 M2 横向布局时宽度分割
        self.M1_width = int(displaySize[0] * 0.1)
        self.M2_width = int(displaySize[0] * 0.9)
        # M1 纵向100%
        self.M1_length = int(displaySize[1])

        # M1中S1 S2 S3 纵向布局高度分割
        self.M1S1_length = int(self.M1_length * 0.2)
        self.M1S2_length = int(self.M1_length * 0.2)
        self.M1S3_length = int(self.M1_length * 0.6)

        self.BackWebPanel = WebPanel(self)

        # 第二层布局
        self.vbox_sizer_b = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        self.vbox_sizer_b.Add(
            self._init_para_notebook(),
            proportion=1,
            flag=wx.EXPAND | wx.BOTTOM,
            border=5,
        )  # 添加行情参数布局
        # self.vbox_sizer_b.Add(
        #     self.patten_log_tx, proportion=10, flag=wx.EXPAND | wx.BOTTOM, border=5
        # )

        self.vbox_sizer_b.Add(self.BackWebPanel, proportion=10, flag=wx.EXPAND|wx.ALL|wx.CENTER, border=5)

        # 第一层布局
        self.HBoxPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanelSizer.Add(
            self.vbox_sizer_b, proportion=0, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.SetSizer(self.HBoxPanelSizer)  # 使布局有效

        # self.layout()

    def layout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox)

        hbox.Add(wx.StaticText(self, label="请选择基准:"))
        combo_benchmarks = wx.ComboBox(self, size=(190, 25), pos=(10, 120))
        combo_benchmarks.SetItems(["沪深300指数(000300.SH)", "标普500指数(SPY)"])
        hbox.Add(combo_benchmarks)

        # vbox.Add(panel, 0)
        btn = wx.Button(self, label="开始回测", style=1)
        self.Bind(wx.EVT_BUTTON, self.StartBacktest, btn)
        vbox.Add(btn)

        # 底部是一个浏览器
        web = WebPanel(self)
        vbox.Add(web, 1, wx.EXPAND)
        web.show_file(DATA_DIR_BKT_RESULT.joinpath("bkt_result.html"))

        # web.show_url('http://www.jisilu.cn')

        self.web = web

    def _init_para_notebook(self):

        # 创建参数区面板
        self.ParaNoteb = wx.Notebook(self)
        self.ParaStPanel = wx.Panel(self.ParaNoteb, -1)  # 行情
        self.ParaBtPanel = wx.Panel(self.ParaNoteb, -1)  # 回测 back test
        self.ParaPtPanel = wx.Panel(self.ParaNoteb, -1)  # 条件选股 pick stock
        self.ParaPaPanel = wx.Panel(self.ParaNoteb, -1)  # 形态选股 patten

        # 第二层布局
        # self.ParaStPanel.SetSizer(self.add_stock_para_lay(self.ParaStPanel))
        self.ParaBtPanel.SetSizer(self.add_backt_para_lay(self.ParaBtPanel))
        # self.ParaPtPanel.SetSizer(self.add_pick_para_lay(self.ParaPtPanel))
        # self.ParaPaPanel.SetSizer(self.add_patten_para_lay(self.ParaPaPanel))

        # self.ParaNoteb.AddPage(self.ParaStPanel, "行情参数")
        self.ParaNoteb.AddPage(self.ParaBtPanel, "回测参数")
        # self.ParaNoteb.AddPage(self.ParaPtPanel, "条件选股")
        # self.ParaNoteb.AddPage(self.ParaPaPanel, "形态选股")

        return self.ParaNoteb

    def add_backt_para_lay(self, sub_panel):

        # 回测参数
        back_para_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 行情参数——输入股票基准
        self.stock_benchmark_box = wx.StaticBox(sub_panel, -1, "回测基准选取")
        self.stock_benchmark_sizer = wx.StaticBoxSizer(
            self.stock_benchmark_box, wx.VERTICAL
        )
        self.stock_benchmark_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=["沪深300指数(000300.SH)", "标普500指数(SPX)", "恒生指数(HSI)"],
        )
        self.stock_benchmark_cbox.SetSelection(0)
        # self.stock_benchmark_cbox.Bind(wx.EVT_COMBOBOX, self._on_combobox_benchmarks_changed)  # noqa: E501
        self.select_benchmark = self.stock_benchmark_cbox.GetValue()
        self.benchmark_code = extract_content(self.select_benchmark)[0]
        logger.debug(f"select_benchmark: {self.benchmark_code}")
        self.backtest_opts["benchmark"] = self.benchmark_code
        self.stock_benchmark_sizer.Add(
            self.stock_benchmark_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——初始资金
        self.init_cash_box = wx.StaticBox(sub_panel, -1, "初始资金")
        self.init_cash_sizer = wx.StaticBoxSizer(self.init_cash_box, wx.VERTICAL)
        self.init_cash_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["init_cash"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_init_cash_changed, self.init_cash_input)
        self.init_cash_sizer.Add(
            self.init_cash_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_stake_box = wx.StaticBox(sub_panel, -1, "交易规模")
        self.init_stake_sizer = wx.StaticBoxSizer(self.init_stake_box, wx.VERTICAL)
        self.init_stake_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["stake"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_stake_changed, self.init_stake_input)
        self.init_stake_sizer.Add(
            self.init_stake_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_slippage_box = wx.StaticBox(sub_panel, -1, "滑点")
        self.init_slippage_sizer = wx.StaticBoxSizer(
            self.init_slippage_box, wx.VERTICAL
        )
        self.init_slippage_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["slippage"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_slippage_changed, self.init_slippage_input)
        self.init_slippage_sizer.Add(
            self.init_slippage_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_commission_box = wx.StaticBox(sub_panel, -1, "手续费")
        self.init_commission_sizer = wx.StaticBoxSizer(
            self.init_commission_box, wx.VERTICAL
        )
        self.init_commission_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["commission"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_commission_changed, self.init_commission_input)
        self.init_commission_sizer.Add(
            self.init_commission_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        self.init_tax_box = wx.StaticBox(sub_panel, -1, "印花税")
        self.init_tax_sizer = wx.StaticBoxSizer(self.init_tax_box, wx.VERTICAL)
        self.init_tax_input = wx.TextCtrl(
            sub_panel, -1, str(self.backtest_config["stamp_duty"]), style=wx.TE_LEFT
        )
        # self.Bind(wx.EVT_TEXT, self._on_stamp_duty_changed, self.init_tax_input)
        self.init_tax_sizer.Add(
            self.init_tax_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 行情参数——回测策略选择
        self.stock_strategy_box = wx.StaticBox(sub_panel, -1, "回测策略选取")
        self.stock_strategy_sizer = wx.StaticBoxSizer(
            self.stock_strategy_box, wx.HORIZONTAL
        )
        self.stock_strategy_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=list(strategy_choices)[0],
            style=wx.CB_READONLY | wx.CB_DROPDOWN,
        )
        self.stock_strategy_cbox.SetSelection(0)
        self.stock_strategy_sizer.Add(
            self.stock_strategy_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        # self.stock_strategy_cbox.Bind(wx.EVT_RADIOBUTTON, self._ev_src_choose)
        # self.stock_strategy_cbox.Bind(wx.EVT_COMBOBOX, self._on_combobox_strategy_changed)
        select_strategy = self.stock_strategy_cbox.GetStringSelection()
        self.backtest_opts["select_strategy"] = select_strategy
        logger.debug(f"select_strategy: {select_strategy}")

        # 回测按钮
        self.start_back_but = wx.Button(sub_panel, -1, "开始回测")
        self.start_back_but.SetBackgroundColour(wx.Colour(76, 187, 23))  # 设置背景颜色
        # self.start_back_but.Bind(wx.EVT_BUTTON, self._ev_start_run)  # 绑定按钮事件
        self.start_back_but.Bind(wx.EVT_BUTTON, self.StartBacktest)  # 绑定按钮事件

        # 交易日志
        self.trade_log_but = wx.Button(sub_panel, -1, "交易日志")
        # self.trade_log_but.Bind(wx.EVT_BUTTON, self._ev_trade_log)  # 绑定按钮事件

        self.BackWebPanel.show_file(DATA_DIR_BKT_RESULT.joinpath("bkt_result.html"))

        back_para_sizer.Add(
            self.stock_benchmark_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_cash_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_stake_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_slippage_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_commission_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.init_tax_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.stock_strategy_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.start_back_but,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        back_para_sizer.Add(
            self.trade_log_but,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )

        return back_para_sizer

    def _ev_trade_log(self, event):
        pass

    def StartBacktest(self, event):
        print("在线回测属于付费功能，请联系微信：Yida_Zhang2")
        pass

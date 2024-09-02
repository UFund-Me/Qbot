#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import wx

from qbot.gui.panels.panel_real_trade import RealTradePanel
from qbot.gui.panels.panel_sim_trade import SimTradePanel

# from qbot.gui.panels.panel_focus_symbs import FocusSymsPanel


class TradePanel(wx.Panel):
    def __init__(self, parent):
        super(TradePanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.trade_tabs = wx.Notebook(self)

        # self.trade_tabs.AddPage(FocusSymsPanel(self.trade_tabs), "我的自选(预留)")

        sim_trade_opts = {
            "class": "虚拟盘",
            "platform": "东方财富",
            "trade_type": "股票",
            "trade_code": "399006.SZ",
            "strategy": "单因子-相对强弱指数RSI",
        }
        self.trade_tabs.AddPage(SimTradePanel(self.trade_tabs, sim_trade_opts), "模拟交易")

        real_trade_opts = {
            "class": "实盘",
            "platform": "东方财富",
            "trade_type": "股票",
            "trade_code": "399006.SZ",
            "strategy": "单因子-相对强弱指数RSI",
        }
        self.trade_tabs.AddPage(
            RealTradePanel(self.trade_tabs, real_trade_opts), "实盘交易"
        )

        self.trade_tabs.SetSelection(1)

        vbox.Add(self.trade_tabs, 1, flag=wx.EXPAND | wx.ALL, border=5)

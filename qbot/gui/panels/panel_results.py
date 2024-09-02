"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-05-14 18:18:42
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2024-03-29 11:49:42
FilePath: /qbot_pro/qbot/gui/panels/results.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description:

Copyright (c) 2023 by Charmve, All Rights Reserved.
Licensed under the MIT License.
"""

import wx

from qbot.common.logging.logger import LOGGER as logger
from qbot.gui.widgets.widget_web import WebPanel
from qbot.gui.widgets.widgets import MatplotlibPanel, PandasGrid


class ResultsPanel(wx.Panel):
    def __init__(self, parent):
        super(ResultsPanel, self).__init__(parent)
        self.init_tabs()

    def handle_data(self, data_dict):
        logger.info(f"{data_dict.keys()}")
        if "raw" in data_dict.keys():
            # logger.debug('data_dict["raw"]: ')
            # print(data_dict["raw"])
            self.panel_raw.show_df(data_dict["raw"])

            self.tabs.SetSelection(0)

        if "features" in data_dict.keys():
            self.panel_features.show_df(data_dict["features"])

            self.tabs.SetSelection(3)

        if "ratio" in data_dict.keys():
            self.pd.show_df(data_dict["ratio"])

        if "corr" in data_dict.keys():
            # print("corr: ", corr)
            self.pd_corr.show_df(data_dict["corr"])

        if "plot" in data_dict.keys():
            plot = data_dict["plot"]
            # print("plot: ", plot)
            self.plot.show_data(plot)

        if "indicator" in data_dict.keys():
            logger.debug("plot_file: {}".format(data_dict["indicator"]))
            plot_kline_file = data_dict["indicator"]
            self.kline_plot.show_file(plot_kline_file)

            self.tabs.SetSelection(1)

        if "bolling" in data_dict.keys():
            logger.debug("plot_file: {}".format(data_dict["bolling"]))
            plot_kline_boll_file = str(data_dict["bolling"])
            self.kline_boll_plot.show_file(plot_kline_boll_file)

        if "yearly" in data_dict.keys():
            yearly = data_dict["yearly"]
            self.pd_yearly.show_df(yearly)

        # self.pd.show_df()

    def init_tabs(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.tabs = wx.Notebook(self)
        vbox.Add(self.tabs, 1, wx.EXPAND)

        self.panel_raw = PandasGrid(self.tabs)
        self.panel_features = PandasGrid(self.tabs, nrow=1000, ncol=20)

        panel_tab = wx.Panel(self.tabs)
        panel_yearly = wx.Panel(self.tabs)
        panel_corr = wx.Panel(self.tabs)
        panel_plot = wx.Panel(self.tabs)
        panel_kline_plot = wx.Panel(self.tabs)
        panel_kline_boll_plot = wx.Panel(self.tabs)

        self.tabs.AddPage(self.panel_raw, "行情数据")
        self.tabs.AddPage(panel_kline_plot, "可视化数据(K线)")
        self.tabs.AddPage(panel_kline_boll_plot, "可视化数据(布林带)")
        self.tabs.AddPage(self.panel_features, "特征提取")

        self.tabs.AddPage(panel_plot, "序列绘图")
        self.tabs.AddPage(panel_tab, "风险收益")
        self.tabs.AddPage(panel_yearly, "年度收益")
        self.tabs.AddPage(panel_corr, "相关性分析")

        self.pd = PandasGrid(panel_tab, nrow=30, ncol=20)
        self.pd_yearly = PandasGrid(panel_yearly, nrow=30, ncol=20)

        vbox_panel = wx.BoxSizer(wx.VERTICAL)
        vbox_panel.Add(self.pd, 1, wx.EXPAND)

        vbox_yearly = wx.BoxSizer(wx.VERTICAL)
        vbox_yearly.Add(self.pd_yearly, 1, wx.EXPAND)
        panel_tab.SetSizer(vbox_panel)
        panel_yearly.SetSizer(vbox_yearly)

        self.init_corr(panel_corr)
        self.init_plot(panel_plot)
        self.init_kline_plot(panel_kline_plot)
        self.init_kline_boll_plot(panel_kline_boll_plot)

    def init_corr(self, parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.pd_corr = PandasGrid(parent)
        vbox.Add(self.pd_corr, 1, wx.EXPAND)

    def init_plot(self, parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.plot = MatplotlibPanel(parent)
        vbox.Add(self.plot, 1, wx.EXPAND)

    def init_kline_plot(self, parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.kline_plot = WebPanel(parent)
        vbox.Add(self.kline_plot, 1, wx.EXPAND)

    def init_kline_boll_plot(self, parent):
        vbox = wx.BoxSizer(wx.VERTICAL)
        parent.SetSizer(vbox)
        self.kline_boll_plot = WebPanel(parent)
        vbox.Add(self.kline_boll_plot, 1, wx.EXPAND)

    # def init_kline_plot(self, parent):
    #     vbox = wx.BoxSizer(wx.VERTICAL)
    #     self.SetSizer(vbox)

    #     self.tabs = wx.Notebook(self)
    #     vbox.Add(self.tabs, 1, wx.EXPAND)

    #     panel_plot_ma = wx.Panel(self.tabs)
    #     panel_plot_boll = wx.Panel(self.tabs)

    #     self.tabs.AddPage(panel_plot_ma, "K均线")
    #     self.tabs.AddPage(panel_plot_boll, "K线布林带")

    #     self.init_kline_ma_plot(panel_plot_ma)
    #     self.init_kline_boll_plot(panel_plot_boll)

    # def init_kline_ma_plot(self, parent):
    #     vbox = wx.BoxSizer(wx.VERTICAL)
    #     parent.SetSizer(vbox)
    #     parent.kline_plot = WebPanel(parent)
    #     vbox.Add(parent.kline_plot, 1, wx.EXPAND)

    # def init_kline_boll_plot(self, parent):
    #     vbox = wx.BoxSizer(wx.VERTICAL)
    #     parent.SetSizer(vbox)
    #     parent.kline_boll_plot = WebPanel(parent)
    #     vbox.Add(parent.kline_boll_plot, 1, wx.EXPAND)

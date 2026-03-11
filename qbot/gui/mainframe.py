import os
import time
from pathlib import Path

import wx

from qbot.gui.elements.def_dialog import ParamsConfigDialog
from qbot.gui.panels.panel_backtest import PanelBacktest
from qbot.gui.panels.panel_trade import TradePanel
from qbot.gui.panels.panel_zhiku import ZhikuPanel
from qbot.gui.widgets.widget_web import WebPanel
from qbot.version import version

# from qbot.gui.panels.panel_userframe import UserFrame
# from qbot.gui.panels.actions import ActionsPanel
# from qbot.gui.panels.page_timeseries import PageTimeSeries
# from qbot.gui.panels.panels import TimeSeriesAnalysis


TOP_DIR = Path(__file__).parent.parent
APP_NAME = "Qbot - AI Quant Robot"


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        displaySize = wx.DisplaySize()
        displaySize = 0.75 * displaySize[0], 0.70 * displaySize[1]
        super().__init__(parent=None, title="Qbot - AI智能量化投研平台", size=displaySize)

        # 设置程序图标
        icon_file = "qbot/gui/imgs/logo.ico"
        icon = wx.Icon(icon_file, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.init_statusbar()
        self.init_menu_bar()
        self.init_main_tabs()

    def init_menu_bar(self):
        # 创建窗口面板
        menuBar = wx.MenuBar(style=wx.MB_DOCKABLE)
        self.SetMenuBar(menuBar)
        self.SetMinSize((1618, 902))

        setting = wx.Menu()
        menuBar.Append(setting, "&设置")
        params_conf = wx.MenuItem(setting, wx.ID_ANY, "&参数配置")
        setting.Append(params_conf)
        self.Bind(wx.EVT_MENU, self.on_params_conf, params_conf)

        tools = wx.Menu()
        menuBar.Append(tools, "&工具")

        valuation = wx.MenuItem(tools, 1, "&蛋卷估值")
        tools.Append(valuation)
        self.Bind(wx.EVT_MENU, self.on_menu, valuation)
        tools.AppendSeparator()
        jisilu = wx.MenuItem(tools, 2, "&集思录")
        tools.Append(jisilu)
        self.Bind(wx.EVT_MENU, self.on_menu, jisilu)
        monitoring = wx.MenuItem(tools, 3, "&后台监控")
        tools.Append(monitoring)
        self.Bind(wx.EVT_MENU, self.start_monitoring, monitoring)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, "关于")
        menuBar.Append(helpMenu, "&帮助")
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def on_menu(self, event):
        web = WebPanel(self.tabs)
        if event.Id == 1:
            web.show_url("https://danjuanapp.com/djmodule/value-center")
        if event.Id == 2:
            web.show_url("https://www.jisilu.cn/")

    def on_params_conf(self, event):
        dialog = ParamsConfigDialog(self)
        dialog.Show()

    def OnAbout(self, event):
        wx.MessageBox(
            "公众号: 迈微AI研习社",
            "关于 Qbot智能量化投研平台",
            wx.OK | wx.ICON_INFORMATION,
        )

    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()  # 创建状态条
        # 将状态栏分割为3个区域,比例为4:1
        self.statusBar.SetFieldsCount(3)
        self.statusBar.SetStatusWidths([-4, -1, -1])
        t = time.localtime(time.time())
        self.SetStatusText("欢迎使用AI智能量化投研平台！请关注公众号: 迈微AI研习社", 0)
        self.SetStatusText("当前版本：%s" % str(version), 1)
        self.SetStatusText(time.strftime("%Y-%B-%d %I:%M:%S", t), 2)

        self.sys_timer = wx.Timer(self, id=wx.ID_ANY)
        self.sys_timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self._update_sys_time, self.sys_timer)

    def _update_sys_time(self, event):
        t = time.localtime(time.time())
        self.SetStatusText(time.strftime("%Y-%B-%d %I:%M:%S", t), 2)

    def start_monitoring(self, event):
        monitor_pids = grep_pid("monitoring")
        if not monitor_pids:
            for pid in monitor_pids:
                os.system(f"kill -9 {pid}")
        os.system("nohup python qbot/plugins/auto_monitor.py > monitoring.log &")
        wx.MessageBox("股票监控程序已开启，后台查看日志。 'tail -f monitoring.log' ")

    def init_main_tabs(self):
        # self.SetBackgroundColour(wx.GREEN)
        # 创建水平boxsizer，并设置为平铺到整个窗口
        self.boxH = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.boxH)

        # 主窗口notebook
        self.tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.boxH.Add(self.tabs, 1, wx.ALL | wx.EXPAND)  # todo propotion==1为何

        self.tabs.AddPage(ZhikuPanel(self.tabs), "Qbot 投研智库", True)

        web1 = WebPanel(self.tabs)
        self.tabs.AddPage(web1, "ChatGPT 策略编写", True)
        web1.show_url("https://wo2qwg.aitianhu.com/")

        web2 = WebPanel(self.tabs)
        self.tabs.AddPage(web2, "AI 选股/选基", True)
        web2.show_url("http://111.229.117.200:4868")

        web3 = WebPanel(self.tabs)
        self.tabs.AddPage(web3, "基金投资策略分析", True)
        web3.show_url("https://ufund-me.github.io/funds-web/#/")

        # TODO(Charmve):
        # 多线程实现提高系统启动速度
        self.tabs.AddPage(PanelBacktest(self.tabs), "可视化股票/基金回测系统", True)

        # web4 = WebPanel(self.tabs)
        # self.tabs.AddPage(web4, "交易策略在线交易", True)
        # web4.show_url("https://sim.myquant.cn/sim?acc=5e4cdda3-f2fb-11ed-ae27-00163e022aa6")

        # self.tabs.AddPage(UserFrame(self.tabs), "Qbot 量化投研", True)
        # self.tabs.AddPage(ActionsPanel(self.tabs), "资产轮动策略分析", True)
        self.tabs.AddPage(TradePanel(self.tabs), "在线交易(实盘/虚拟盘)", True)

        self.tabs.SetSelection(4)  # 可视化股票/基金回测系统 as hometab

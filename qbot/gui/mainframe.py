import os
import subprocess
import threading
import time
from pathlib import Path

import matplotlib.pyplot as plt
import psutil
import wx

from qbot.gui.panels.panel_backtest import PanelBacktest
# from qbot.gui.panels.panel_trade import TradePanel
# from qbot.gui.panels.panel_userframe import UserFrame
from qbot.gui.panels.panel_zhiku import ZhikuPanel
# from qbot.gui.panels.actions import ActionsPanel
# from qbot.gui.panels.page_timeseries import PageTimeSeries
# from qbot.gui.panels.panels import TimeSeriesAnalysis

from qbot.gui.widgets.widget_web import WebPanel
from qbot.version import version

TOP_DIR = Path(__file__).parent.parent
APP_NAME = "Qbot - AI Quant Robot"


class ShellThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        subprocess.call(self.command, shell=True)


def run_notebook_local():
    cmd = "cd ~/Qbot/backend/pytrader/strategies/ && jupyter-notebook"
    t = ShellThread(cmd)
    t.start()
    # os.system(cmd)
    # subprocess.call(cmd)


def grep_pid(key="investool"):
    all_processes = psutil.process_iter()
    investool_processes = [p for p in all_processes if key in p.name()]
    pids = [p.pid for p in investool_processes]
    return pids


def get_investool_bin():
    import platform

    system_name = platform.system()
    investoll_bin = "investool"
    if system_name == "Darwin":  # MacOs
        investoll_bin = "investool_app_mac"
    elif system_name == "Linux":
        ubuntu_version = os.system("uname -a | grep Ubuntu | awk '{print $4}'")
        if "22.04" in ubuntu_version:
            investoll_bin = "investool_ubuntu22"
        elif "18.04" in ubuntu_version:
            investoll_bin = "investool_ubuntu18"
        else:
            print("investool 目前只支持mac、ubuntu22、ubuntu18.04")
        os.system(f"notify-send ['Qbot - {symbol}{type}'] '{symbol}当前价格为{price}'")
    else:
        print("investool 目前只支持mac、ubuntu22、ubuntu18.04")
    return investoll_bin


def run_qinvestool():
    investool_pids = grep_pid("investoll")
    if not investool_pids:
        for pid in investool_pids:
            os.system(f"kill -9 {pid}")

    print("Start QInvesTool ...")
    investoll_bin = get_investool_bin()

    if os.getenv("QBOT_RELEASE") == 1:
        cmd = f"cd backend/investool && ./{investoll_bin} webserver"
        os.system(cmd)
    else:
        shell_thread = ShellThread(
            "cd backend/investool && go build && ./main webserver"
        )
        shell_thread.start()

    cmd = "cd backend/investool && ./investool json -d"  # dump funds json data
    os.system(cmd)


def run_fund_tool():
    print("Start fund strategy analyse server ...")
    t = ShellThread(
        "docker run -dp 8000:8000 fund_strategy --name=fund_strategy_instance"
    )
    t.start()
    # cmd = ''
    # subprocess.call(cmd)
    # os.system(cmd)


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        displaySize = wx.DisplaySize()
        displaySize = 0.75 * displaySize[0], 0.70 * displaySize[1]
        super().__init__(parent=None, title="Qbot - AI量化投研平台", size=displaySize)

        # 设置程序图标
        icon_file = "qbot/gui/imgs/logo.ico"
        icon = wx.Icon(icon_file, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 屏幕居中显示
        self.SetMenuBar(self.make_menubar(self))
        self.SetMinSize((1448, 802))

        self.init_statusbar()
        # self.init_menu_bar()
        self.init_main_tabs()

    def __del__(self):
        # win.Close(True)
        self.Destroy()

    def OnAbout(self, event):
        wx.MessageBox(
            "公众号: 迈微AI研习社",
            "关于 Qbot智能量化投研平台",
            wx.OK | wx.ICON_INFORMATION,
        )

    def OnExit(event):
        # win.Close(True)
        self.Destroy()

    def init_menu_bar(self):
        # 屏幕居中显示
        self.Centre()
        self.SetMenuBar(self.make_menubar(self))
        # self.Maximize()

    def make_menubar(self, win):
        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT, "退出")
        menuBar.Append(fileMenu, "&菜单")

        tools = wx.Menu()
        menuBar.Append(tools, "&工具")

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, "关于")
        menuBar.Append(helpMenu, "&帮助")

        valuation = wx.MenuItem(tools, 1, "&蛋卷估值")
        tools.Append(valuation)
        self.Bind(wx.EVT_MENU, self.on_menu, valuation)

        tools.AppendSeparator()

        jisilu = wx.MenuItem(tools, 2, "&集思录")
        tools.Append(jisilu)
        self.Bind(wx.EVT_MENU, self.on_menu, jisilu)

        monitoring = wx.MenuItem(tools, 1, "&后台监控")
        tools.Append(monitoring)
        self.Bind(wx.EVT_MENU, self.monitoring, monitoring)

        win.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        win.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        return menuBar

    def on_menu(self, event):
        web = WebPanel(self.tabs)
        if event.Id == 1:
            web.show_url("https://danjuanapp.com/djmodule/value-center")
        if event.Id == 2:
            web.show_url("https://www.jisilu.cn/")

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

    def monitoring(self, event):
        monitor_pids = grep_pid("monitoring")
        if not monitor_pids:
            for pid in monitor_pids:
                os.system(f"kill -9 {pid}")
        os.system("python monitoring.py > qmonitoring.log")
        wx.MessageBox("股票监控程序已开启，后台查看日志。 'tail -f qmonitoring.log' ")

    def init_main_tabs(self):
        # self.SetBackgroundColour(wx.GREEN)
        # 创建水平boxsizer，并设置为平铺到整个窗口
        self.boxH = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.boxH)

        # 主窗口notebook
        self.tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.boxH.Add(self.tabs, 1, wx.ALL | wx.EXPAND)  # todo propotion==1为何

        self.tabs.AddPage(ZhikuPanel(self.tabs), "Qbot 投研智库", True)

        web = WebPanel(self.tabs)
        self.tabs.AddPage(web, "ChatGPT 策略编写", True)
        web.show_url("https://wo2qwg.aitianhu.com/")

        plt.rc("grid", color="#316931", linewidth=1, linestyle="-")
        plt.rc("xtick", labelsize=15)
        plt.rc("ytick", labelsize=15)

        web = WebPanel(self.tabs)
        self.tabs.AddPage(web, "AI 选股/选基", True)
        web.show_url("http://111.229.117.200:4868")

        web = WebPanel(self.tabs)
        self.tabs.AddPage(web, "基金投资策略分析", True)
        web.show_url("https://ufund-me.github.io/funds-web/#/")

        # web = WebPanel(self.tabs)
        # self.tabs.AddPage(web, "我的自选", True)
        # attention_file = (
        #     os.path.dirname(__file__) + "/../../frontend/web-extension/index.html"
        # )
        # web.show_file(attention_file)

        #TODO(Charmve): 
        # 多线程实现提高系统启动速度
        
        self.tabs.AddPage(PanelBacktest(self.tabs), "可视化股票/基金回测系统", True)

        web = WebPanel(self.tabs)
        self.tabs.AddPage(web, "交易策略在线交易", True)
        web.show_url("https://sim.myquant.cn/sim?acc=5e4cdda3-f2fb-11ed-ae27-00163e022aa6")

        # self.tabs.AddPage(UserFrame(self.tabs), "Qbot 量化投研", True)

        # self.tabs.AddPage(ActionsPanel(self.tabs), "资产轮动策略分析", True)

        # self.tabs.AddPage(TradePanel(self.tabs), "在线交易(实盘/虚拟盘)", True)

        self.tabs.SetSelection(4)  # 可视化股票/基金回测系统 as hometab

    def Destroy(self):
        return True
        pass

import os
from pathlib import Path

import matplotlib.pyplot as plt
import wx
import subprocess
import threading

from gui.panels.panel_backtest import PanelBacktest

# from gui.widgets.widget_matplotlib import MatplotlibPanel
from gui.widgets.widget_web import WebPanel

TOP_DIR = Path(__file__).parent.parent.parent.joinpath("Qbot")
APP_NAME = "Qbot - Quant AI Robot"


def OnAbout(event):
    wx.MessageBox("公众号:迈微AI研习社", "关于 AI量化投研平台", wx.OK | wx.ICON_INFORMATION)


def OnExit(win, event):
    win.Close(True)


def make_menubar(win):
    # Make a file menu with Hello and Exit items
    fileMenu = wx.Menu()
    # The "\t..." syntax defines an accelerator key that also triggers
    # the same event
    helloItem = fileMenu.Append(
        -1, "&Hello...\tCtrl-H", "Help string shown in status bar for this menu item"
    )
    fileMenu.AppendSeparator()
    # When using a stock ID we don't need to specify the menu item's
    # label
    exitItem = fileMenu.Append(wx.ID_EXIT, "退出")

    # Now a help menu for the about item
    helpMenu = wx.Menu()
    aboutItem = helpMenu.Append(wx.ID_ABOUT, "关于")

    menuBar = wx.MenuBar()
    menuBar.Append(fileMenu, "&文件")
    menuBar.Append(helpMenu, "&帮助")

    win.Bind(wx.EVT_MENU, OnAbout, aboutItem)
    win.Bind(wx.EVT_MENU, OnExit, exitItem)
    return menuBar


class ShellThread(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        subprocess.call(self.command, shell=True)

def run_notebook_local():
    cmd = ''
    t = ShellThread("cd ~/Qbot/pytrader/strategies/ && jupyter-notebook")
    t.start()
    # os.system(cmd)
    # subprocess.call(cmd)

def run_invest_tool():
    print("Start QInvesTool ...")
    t = ShellThread("cd ~/Qbot/investool && go build && ./investool webserver")
    t.start()
    # cmd = ''
    # # subprocess.call(cmd)
    # os.system(cmd)

def run_fund_tool(): 
    print("Start fund strategy analyse server ...")
    t = ShellThread("docker run -dp 8000:8000 fund_strategy --name=fund_strategy_instance")
    t.start()
    # cmd = ''
    # subprocess.call(cmd)
    # os.system(cmd)

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        # 设置默认大小
        self.SetSize(wx.Size(600, 400))
        self.SetName(APP_NAME)

        # 设置程序图标
        icon_file = os.path.join(
            os.path.abspath(TOP_DIR.joinpath("gui/imgs")), "logo.ico"
        )
        icon = wx.Icon(icon_file, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 屏幕居中显示
        self.Centre()
        self.SetMenuBar(make_menubar(self))
        self.Maximize()

        self.CreateStatusBar()
        self.SetStatusText("欢迎使用AI智能量化投研平台！请关注公众号:迈微AI研习社")

        # 主窗口notebook
        self.m_notebook = wx.Notebook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0
        )

        homepage = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(homepage, "Qbot 官方网站", True)
        homepage.show_url("https://ufund-me.github.io/Qbot")

        plt.rc("grid", color="#316931", linewidth=1, linestyle="-")
        plt.rc("xtick", labelsize=15)
        plt.rc("ytick", labelsize=15)

        # plot = MatplotlibPanel(self.m_notebook)
        # self.m_notebook.AddPage(plot, "基金投资策略分析", True)
        # plot.show()

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "AI 选股/选基", True)
        # run_invest_tool()
        web.show_url("http://localhost:4868/")
        # web.show_url("https://investool.axiaoxin.com/?from=github")

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "交易策略在线交易", True)
        # bash: cd ~/Qbot/pytrader/strategies/ && jupyter-notebook
        # run_notebook_local()
        # web.show_url("http://localhost:8888/tree")
        web.show_url("https://sim.myquant.cn/sim?acc=5e4cdda3-f2fb-11ed-ae27-00163e022aa6")

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "基金投资策略分析", True)
        # run_fund_tool()
        # web.show_url("http://locahost:8000")
        web.show_url("http://sunshowerc.github.io/fund/#/")

        self.m_notebook.AddPage(PanelBacktest(self.m_notebook), "可视化股票回测系统", True)

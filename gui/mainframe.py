import wx
from gui.panels.panel_backtest import PanelBacktest
from gui.widgets.widget_web import WebPanel


def OnAbout(event):
    wx.MessageBox("公众号:迈微AI研习社",
                  "关于 AI量化投研平台",
                  wx.OK | wx.ICON_INFORMATION)


def OnExit(win, event):
    win.Close(True)


def make_menubar(win):
    # Make a file menu with Hello and Exit items
    fileMenu = wx.Menu()
    # The "\t..." syntax defines an accelerator key that also triggers
    # the same event
    helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                                "Help string shown in status bar for this menu item")
    fileMenu.AppendSeparator()
    # When using a stock ID we don't need to specify the menu item's
    # label
    exitItem = fileMenu.Append(wx.ID_EXIT, '退出')

    # Now a help menu for the about item
    helpMenu = wx.Menu()
    aboutItem = helpMenu.Append(wx.ID_ABOUT, '关于')

    menuBar = wx.MenuBar()
    menuBar.Append(fileMenu, "&文件")
    menuBar.Append(helpMenu, "&帮助")

    win.Bind(wx.EVT_MENU, OnAbout, aboutItem)
    win.Bind(wx.EVT_MENU, OnExit, exitItem)
    return menuBar


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        # 设置默认大小
        self.SetSize(wx.Size(900, 600))

        # # 设置程序图标
        # icon = wx.Icon('./imgs/logo.ico', wx.BITMAP_TYPE_ICO)
        # self.SetIcon(icon)

        # 屏幕居中显示
        self.Centre()
        self.SetMenuBar(make_menubar(self))
        self.Maximize()

        self.CreateStatusBar()
        self.SetStatusText("欢迎使用AI智能量化投研平台！请关注公众号:迈微AI研习社")

        # 主窗口notebook
        self.m_notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, '官方网站', True)
        web.show_url('ufund-me.github.io')
        # web.show_url('http://localhost:8888/notebooks/examples/workflow_by_code.ipynb?token=d6526946101b02f1755058d5f76a18a5f4117d5c6857249b')

        self.m_notebook.AddPage(PanelBacktest(self.m_notebook), "可视化回测系统", True)


# -*- coding:utf-8 -*-

import os

import wx
import wx.adv

from qbot.common.config import RESEARCH_REPORTS
from qbot.common.file_utils import list_files_in_directory
from qbot.common.logging.logger import LOGGER as logger
from qbot.common.utils import check_port_in_use
from qbot.gui.widgets.widget_web import WebPanel


class QbotHomePanel(wx.Panel):
    def __init__(self, parent):
        super(QbotHomePanel, self).__init__(parent)
        self.init_ui()

    def __del__(self):
        pass

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)
        # self.boxH = wx.BoxSizer(wx.HORIZONTAL)
        # self.SetSizer(self.boxH)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        # self.hbox.Add(wx.StaticText(self, label="Qbot 官方网站"))
        vbox.Add(self.hbox)

        # # 主窗口notebook
        # self.tabs = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        # self.boxH.Add(self.tabs, 1, wx.ALL | wx.EXPAND)  # todo propotion==1为何
        # vbox.Add(self.boxH)

        homepage = WebPanel(self)
        # self.tabs.AddPage(homepage, "Qbot 官方网站", True)
        vbox.Add(homepage, 1, wx.EXPAND)
        homepage.show_url("https://ufund-me.github.io/Qbot")


class YanbaoPanel(wx.Panel):
    def __init__(self, parent):
        super(YanbaoPanel, self).__init__(parent)
        self.reports_url = "http://111.229.117.200:9080/"

        self.init_reports_httpserver()
        self.init_ui()

    def __del__(self):
        pass

    def init_reports_httpserver(self):
        if not check_port_in_use(port=9080):
            os.popen(f"python -m http.server --directory {RESEARCH_REPORTS} 9080")
        self.reports_url = "http://localhost:9080/"

    def init_ui(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(self.hbox)

        self.hbox.Add(wx.StaticText(self, label="证券投资研报库"))
        self.combo_yanbao = wx.ComboBox(self, size=(190, 24))
        self.combo_yanbao.Bind(wx.EVT_COMBOBOX, self.on_combobox_yanbao_changed)
        self.yanbao_files = list_files_in_directory(RESEARCH_REPORTS, [".pdf"])
        # logger.debug(f"研报数据: {self.yanbao_files}")
        self.combo_yanbao.SetItems(self.yanbao_files)
        self.combo_yanbao.SetValue("【华泰金工】多因子10：因子合成方法实证分析20190104")
        self.hbox.Add(self.combo_yanbao)
        yanbao_file = self.combo_yanbao.GetValue()
        # logger.debug(f"select_strategy: {yanbao_file}")

        self.page_view = WebPanel(self)
        self.vbox.Add(self.page_view, 1, wx.EXPAND)
        # self.tabs.AddPage(page_view, "Qbot 官方网站", True)

        if yanbao_file:
            file_name = "{}{}".format(yanbao_file, ".pdf")
            logger.debug(file_name)
            file_url = self.reports_url + file_name
            self.page_view.show_url(file_url)
        else:
            self.page_view.show_url(
                "https://crm.htsc.com.cn/doc/2020/10750101/d287ebf2-7f3f-4382-bf3f-cfabd4b90161.pdf"  # noqa: E501
            )

    def on_combobox_yanbao_changed(self, event):
        yanbao_file = self.combo_yanbao.GetValue()
        logger.info(f"研报数据: You select {yanbao_file}")

        if yanbao_file:
            file_name = "{}{}".format(yanbao_file, ".pdf")
            logger.debug(file_name)
            file_url = self.reports_url + file_name
            self.page_view.show_url(file_url)
        else:
            self.page_view.show_url(
                "https://crm.htsc.com.cn/doc/2020/10750101/d287ebf2-7f3f-4382-bf3f-cfabd4b90161.pdf"  # noqa: E501
            )


class NotebookPanel(wx.Panel):
    def __init__(self, parent):
        super(NotebookPanel, self).__init__(parent)
        self.iSNotebookActive = False
        self.local_notebook_url = "http://localhost:8800/tree"  # noqa: E501
        self.init_ui()

    def __del__(self):
        pass

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        start_btn = wx.Button(self, -1, label="运行在线Notebook")
        vbox.Add(start_btn, 0)
        self.Bind(wx.EVT_BUTTON, self.start_notebook, start_btn)

        self.notebook_page = WebPanel(self)
        vbox.Add(self.notebook_page, 1, wx.EXPAND)

        if self.iSNotebookActive:
            self.notebook_page.show_url(self.local_notebook_url)

    def start_notebook(self, event):
        logger.info("start show onlite notebook ...")
        logger.info(self.local_notebook_url)
        self.notebook_page.show_url(self.local_notebook_url)

    def start_online_notebook(self):
        os.popen("jupyter notebook --no-browser --port 8800 ./docs/notebook")
        self.iSNotebookActive = True

    # def start_online_notebook(self):
    #     import re
    #     logs = os.popen(f"jupyter notebook --no-browser --port 8800 ./docs/notebook")
    #     token_pattern = r'(?<=\?token=)[a-zA-Z0-9]+'
    #     tokens = re.findall(token_pattern, logs)
    #     return tokens[0]


class ZhikuPanel(wx.Panel):
    def __init__(self, parent):
        super(ZhikuPanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.tabs = wx.Notebook(self)
        self.tabs.AddPage(QbotHomePanel(self.tabs), "Qbot 官方网站")
        self.tabs.AddPage(YanbaoPanel(self.tabs), "证券投资研报")
        self.tabs.AddPage(NotebookPanel(self.tabs), "在线代码运行notebook")

        vbox.Add(self.tabs, 1, flag=wx.EXPAND | wx.ALL, border=5)

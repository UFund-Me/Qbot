#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import wx
import wx.adv
import wx.grid
import wx.html2

from qbot.common.logging.logger import LOGGER as logger

# 分离控件事件中调用的子事件
from qbot.common.macros import (
    btc_trade_platforms,
    futures_trade_platforms,
    strategy_choices,
    trade_platforms,
)

# from qbot.engine.config import MULTI_FACTS_DIR
from qbot.engine.trade.trade_engine import TradeEngine

# from qbot.gui.common.CodePool import ManageCodePool
# from qbot.gui.common.CodeTable import ManageCodeTable
from qbot.gui.common.PrintLog import SysLogIf

# from qbot.gui.common.SysFile import Base_File_Oper
from qbot.gui.elements.def_dialog import MessageDialog, UserDialog
from qbot.gui.elements.def_grid import GridTable
from qbot.gui.elements.def_treelist import CollegeTreeListCtrl
from qbot.gui.widgets.widget_web import WebPanel

# from qbot.strategy.strategy_gath.StrategyGath import Base_Strategy_Group


plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号


class RealTradePanel(wx.Panel):
    def __init__(
        self, parent=None, trader_opts={}, displaySize=(1600, 900), Fun_SwFrame=None
    ):
        super(RealTradePanel, self).__init__(parent)

        self.ClickNum = 0  # OnClickTrade

        # trade_class = ("虚拟盘")
        # trade_type = ("股票")
        # trade_platform = ("东方财富")
        # trade_code = ("399006.SZ")
        # trade_strategy = ("单因子-相对强弱指数RSI")

        self.trader_opts = {
            "class": trader_opts["class"],
            "platform": trader_opts["platform"],
            "trade_type": trader_opts["trade_type"],
            "trade_code": trader_opts["trade_code"],
            "strategy": trader_opts["strategy"],
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

        # 用于量化工具集成到整体系统中
        self.fun_swframe = Fun_SwFrame

        # 存储单个行情数据
        self.stock_dat = pd.DataFrame()

        # 多子图布局对象
        self.FlexGridSizer = None

        # 存储策略函数
        self.function = ""

        self.trader_class = trader_opts["class"]
        self.multi_facts_config = "ROC(20)动量信号周频Top1"
        self.multi_facts_list = list()
        self.init_ui()

    def init_ui(self):

        # 添加参数布局
        self.vbox_sizer_a = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        self.vbox_sizer_a.Add(
            self._init_text_log(), proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5
        )
        self.vbox_sizer_a.Add(
            self._init_listbox_mult(),
            proportion=1,
            flag=wx.EXPAND | wx.BOTTOM,
            border=5,
        )
        self.vbox_sizer_a.Add(
            self._init_nav_notebook(),
            proportion=2,
            flag=wx.EXPAND | wx.BOTTOM,
            border=5,
        )

        # 创建显示区面板
        self.RealTradeWebPanel = WebPanel(self)

        # 第二层布局
        self.vbox_sizer_b = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        self.vbox_sizer_b.Add(
            self._init_trade_para_notebook(),
            proportion=1,
            flag=wx.EXPAND | wx.BOTTOM,
            border=5,
        )  # 添加行情参数布局
        self.vbox_sizer_b.Add(self.RealTradeWebPanel, 10, wx.EXPAND)

        # 第一层布局
        self.HBoxPanelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanelSizer.Add(
            self.vbox_sizer_a, proportion=1, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.HBoxPanelSizer.Add(
            self.vbox_sizer_b, proportion=10, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.SetSizer(self.HBoxPanelSizer)  # 使布局有效

        # ################################## 辅助配置 ###################################
        self.syslog = SysLogIf(self.sys_log_tx)

        # ################################## 加载股票代码表 ###################################
        # self.code_table = ManageCodeTable(self.syslog)
        # self.code_table.update_stock_code()

        # ################################## 加载自选股票池 ###################################
        # self.code_pool = ManageCodePool(self.syslog)
        # self.grid_pl.SetTable(self.code_pool.load_self_pool(), ["自选股", "代码"])

    def _init_grid_pl(self, subpanel):
        # 初始化股票池表格
        self.grid_pl = GridTable(parent=subpanel, nrow=0, ncol=2)
        self.Bind(
            wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self._ev_click_plcode, self.grid_pl
        )
        return self.grid_pl

    def _ev_click_plcode(self, event):  # 点击股票池股票代码

        # 收集股票池中名称和代码
        st_code = self.grid_pl.GetCellValue(event.GetRow(), 1)
        st_name = self.grid_pl.GetCellValue(event.GetRow(), 0)

        # self.handle_active_code(st_code, st_name)

    def _init_listbox_mult(self):

        self.mult_analyse_box = wx.StaticBox(self, -1, "组合分析股票池")
        self.mult_analyse_sizer = wx.StaticBoxSizer(self.mult_analyse_box, wx.VERTICAL)
        self.listBox = wx.ListBox(
            self,
            -1,
            size=(self.M1_width, self.M1S2_length),
            choices=[],
            style=wx.LB_EXTENDED,
        )
        self.listBox.Bind(wx.EVT_LISTBOX_DCLICK, self._ev_list_select)
        self.mult_analyse_sizer.Add(
            self.listBox, proportion=0, flag=wx.EXPAND | wx.ALL | wx.CENTER, border=2
        )

        return self.mult_analyse_sizer

    def _ev_list_select(self, event):  # 双击从列表中剔除股票

        # 等价与GetSelection() and indexSelected
        if MessageDialog("是否从组合分析股票池中删除该股票？") == "点击Yes":
            indexSelected = event.GetEventObject().GetSelections()
            event.GetEventObject().Delete(indexSelected[0])

    def _init_text_log(self):

        # 创建并初始化系统日志框
        self.sys_log_box = wx.StaticBox(self, -1, "系统日志")
        self.sys_log_sizer = wx.StaticBoxSizer(self.sys_log_box, wx.VERTICAL)
        self.sys_log_tx = wx.TextCtrl(
            self, style=wx.TE_MULTILINE, size=(self.M1_width, self.M1S1_length)
        )
        self.sys_log_sizer.Add(
            self.sys_log_tx, proportion=1, flag=wx.EXPAND | wx.ALL | wx.CENTER, border=2
        )
        return self.sys_log_sizer

    def _init_trade_para_notebook(self):

        # 创建参数区面板
        self.ParaNoteb = wx.Notebook(self)
        self.RealTradePanel = wx.Panel(self.ParaNoteb, -1)  # 实盘交易
        # self.ParaLogPanel = wx.Panel(self.ParaNoteb, -1)  # 交易日志

        # 第二层布局
        self.RealTradePanel.SetSizer(self.add_trade_para_layer(self.RealTradePanel))

        self.ParaNoteb.AddPage(self.RealTradePanel, "实盘交易")

        return self.ParaNoteb

    def add_trade_para_layer(self, sub_panel):

        # 交易参数
        trade_para_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 交易参数——输入交易类型
        self.stocks_select_box = wx.StaticBox(sub_panel, -1, "交易标的")
        self.stocks_select_sizer = wx.StaticBoxSizer(
            self.stocks_select_box, wx.VERTICAL
        )
        self.stocks_select_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=["股票", "基金", "期货", "BTC"],
        )
        self.stocks_select_cbox.SetSelection(0)
        self.stocks_select_cbox.Bind(
            wx.EVT_COMBOBOX, self.on_combobox_trade_type_changed
        )  # noqa: E501
        select_trade_type = self.stocks_select_cbox.GetValue()
        self.trader_opts["trade_type"] = select_trade_type
        logger.debug(f"select_trade_type: {select_trade_type}")
        self.stocks_select_sizer.Add(
            self.stocks_select_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 交易参数——交易标的代码
        self.init_code_box = wx.StaticBox(sub_panel, -1, "交易标的代码")
        self.init_code_sizer = wx.StaticBoxSizer(self.init_code_box, wx.VERTICAL)
        self.init_code_input = wx.TextCtrl(
            sub_panel, -1, str("600519.SH"), style=wx.TE_LEFT  # 贵州茅台
        )
        self.Bind(wx.EVT_TEXT, self._on_input_code_changed, self.init_code_input)
        select_code = self.init_code_input.GetValue()
        logger.debug(f"select_code: {select_code}")
        self.trader_opts["trade_code"] = select_code
        self.init_code_sizer.Add(
            self.init_code_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 交易参数——选择交易平台
        self.trade_platform_box = wx.StaticBox(sub_panel, -1, "选择证券交易平台")
        self.trade_platform_sizer = wx.StaticBoxSizer(
            self.trade_platform_box, wx.VERTICAL
        )
        self.trade_platform_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=list(trade_platforms)[0],
        )
        self.trade_platform_cbox.SetSelection(1)
        self.trade_platform_cbox.Bind(
            wx.EVT_COMBOBOX, self.on_combobox_trade_platform_changed
        )  # noqa: E501
        select_trade_platform = self.trade_platform_cbox.GetValue()
        self.trader_opts["platform"] = select_trade_platform
        logger.debug(f"select_trade_platform: {select_trade_platform}")
        self.trade_platform_sizer.Add(
            self.trade_platform_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 交易参数——交易策略
        self.strategy_select_box = wx.StaticBox(sub_panel, -1, "交易策略选择")
        self.strategy_select_sizer = wx.StaticBoxSizer(
            self.strategy_select_box, wx.VERTICAL
        )
        self.strategy_select_cbox = wx.ComboBox(
            sub_panel,
            -1,
            "",
            choices=list(strategy_choices)[0],
        )
        self.strategy_select_cbox.SetSelection(0)
        self.strategy_select_cbox.Bind(
            wx.EVT_COMBOBOX, self._on_combobox_strategy_changed
        )  # noqa: E501
        select_strategy = self.strategy_select_cbox.GetValue()
        self.trader_opts["strategy"] = select_strategy
        logger.debug(f"[{self.trader_class}] select_trade_strategy: {select_strategy}")
        if "多因子" in select_strategy:
            self.multi_fact_layout()
        self.strategy_select_sizer.Add(
            self.strategy_select_cbox,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 交易按钮
        self.start_trade_butt = wx.Button(sub_panel, -1, "开始交易")
        self.start_trade_butt.SetBackgroundColour(wx.Colour(76, 187, 23))  # 设置背景颜色
        self.start_trade_butt.Bind(wx.EVT_BUTTON, self.OnClickTrade)  # 绑定按钮事件

        # 交易日志
        self.trade_log_butt = wx.Button(sub_panel, -1, "交易日志")
        self.trade_log_butt.Bind(wx.EVT_BUTTON, self._ev_trade_log)  # 绑定按钮事件

        self.show_trade_boardview()

        trade_para_sizer.Add(
            self.stocks_select_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        trade_para_sizer.Add(
            self.init_code_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        trade_para_sizer.Add(
            self.trade_platform_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        trade_para_sizer.Add(
            self.strategy_select_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        trade_para_sizer.Add(
            self.start_trade_butt,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )
        trade_para_sizer.Add(
            self.trade_log_butt,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=5,
        )

        return trade_para_sizer

    def _on_combobox_strategy_changed(self, event):
        select_strategy = self.strategy_select_cbox.GetValue()
        self.trader_opts["strategy"] = select_strategy
        logger.info(f"交易策略: You select {select_strategy}")

    def _on_input_code_changed(self, event):
        select_code = self.init_code_input.GetValue()
        self.trader_opts["trade_code"] = select_code
        logger.info(f"回测股票/基金: You select {select_code}")

    def on_combobox_multi_facts_changed(self, event):
        self.multi_facts_config = self.combo_multi_facts.GetValue()
        logger.info(
            f"[{self.trader_class}] 多因子交易策略: You select {self.multi_facts_config}"
        )
        # self.trader_opts["strategy"] = self.trade_platform

    def on_combobox_trade_type_changed(self, event):
        self.trade_type = self.stocks_select_cbox.GetValue()
        logger.info(f"[{self.trader_class}] 交易类型: You select {self.trade_type}")
        self.trader_opts["trade_type"] = self.trade_type

        if self.trade_type == "股票":
            self.trade_platform_cbox.SetItems(list(trade_platforms)[0])
            self.trader_opts["platform"] = "东方财富"
            self.trade_platform_cbox.SetValue("东方财富")
        elif self.trade_type == "期货":
            self.trade_platform_cbox.SetItems(list(futures_trade_platforms[0]))
            self.trader_opts["platform"] = "CTP"
            self.trade_platform_cbox.SetValue("CTP")

            self.trader_opts["trade_code"] = "zn2409"  # 沪锌2409
            self.init_code_input.SetValue("zn2409")
        elif self.trade_type == "BTC":
            self.trade_platform_cbox.SetItems(list(btc_trade_platforms)[0])
            self.trader_opts["platform"] = "欧易OKX"
            self.trade_platform_cbox.SetValue("欧易OKX")

            self.trader_opts["trade_code"] = "BTCUSDT"
            self.init_code_input.SetValue("BTCUSDT")

        print(self.trader_opts)
        self.show_trade_boardview()

    def on_combobox_trade_platform_changed(self, event):
        self.trade_platform = self.trade_platform_cbox.GetValue()
        logger.info(f"[{self.trader_class}] 交易平台: You select {self.trade_platform}")
        self.trader_opts["platform"] = self.trade_platform

        self.show_trade_boardview()

    def on_combobox_strategy_changed(self, event):
        select_strategy = self.strategy_select_cbox.GetValue()
        self.trader_opts["strategy"] = select_strategy
        logger.info(f"[{self.trader_class}] 交易策略: You select {select_strategy}")
        if "多因子" in select_strategy:
            self.multi_fact_layout()
        else:
            self.remove_multi_fact_layout()

    def OnClickTrade(self, event):

        # MessageDialog("请联系微信：Yida_Zhang2")

        self.start_trade_butt.SetLabel("暂停交易")
        self.ClickNum += 1
        if self.ClickNum % 2 == 1:
            self.start_trade_butt.SetLabel("开始交易")
            self.syslog.re_print("开始实盘交易...\n")
        else:
            self.start_trade_butt.SetLabel("暂停交易")
            self.ClickNum = 0
            logger.info(self.start_trade_butt.GetLabel())
            self.syslog.re_print("暂停实盘交易...\n")
            return

        sim_trade_opts = {
            "class": "实盘",
            "platform": "东方财富",
            "trade_type": "股票",
            "trade_code": "399006.SZ",
            "strategy": "单因子-相对强弱指数RSI",
        }
        # logger.info(self.trader_opts)

        # ######## 开始实盘交易 #########
        self.trade_engine = TradeEngine(self.trader_opts, self.syslog)
        self.trade_engine.login()
        self.trade_engine.get_positions()
        self.trade_engine.start_trade()
        # self.trade_engine.close()

    def show_trade_boardview(self):
        print(
            "$$$$$$$$$$$$\n####",
            self.trader_opts["trade_type"],
            self.trader_opts["class"],
        )
        if self.trader_opts["trade_type"] == "股票":
            juejin_sim = (
                "https://sim.myquant.cn/sim?acc=5e4cdda3-f2fb-11ed-ae27-00163e022aa6"
            )
            self.RealTradeWebPanel.show_url(juejin_sim)
            logger.info(f"RealTradeWebPanel - {juejin_sim}")
        elif self.trader_opts["trade_type"] == "BTC":
            huobi_platform = "https://www.htx.com/zh-cn/grid-exchange/"
            if self.trader_opts["platform"] == "火币Huobi":
                self.RealTradeWebPanel.show_url(huobi_platform)
                logger.info(f"RealTradeWebPanel - {huobi_platform}")
            elif self.trader_opts["platform"] == "欧易OKX":
                okx_url = "https://www.okx.com/zh-hans/trade-spot/btc-usdt"
                self.RealTradeWebPanel.show_url(okx_url)
                logger.info(f"RealTradeWebPanel - {okx_url}")
            elif self.trader_opts["platform"] == "币安Binance":
                binance_url = "https://www.binance.com/zh-CN/trade/BTC_USDT?type=spot"
                self.RealTradeWebPanel.show_url(binance_url)
                logger.info(f"RealTradeWebPanel - {binance_url}")
            else:
                self.RealTradeWebPanel.show_url(
                    "https://www.okx.com/zh-hans/trade-spot/btc-usdt"
                )
                logger.info(
                    "RealTradeWebPanel - https://www.okx.com/zh-hans/trade-spot/btc-usdt"
                )
            # https://crypto-labs.miladsdgh.ir/
        else:
            MessageDialog("交易平台尚未接入，请联系微信：Yida_Zhang2")

    def _ev_trade_log(self, event):

        user_trade_log = UserDialog(self, title="回测提示信息", label="交易详细日志")

        """ 自定义提示框 """
        if user_trade_log.ShowModal() == wx.ID_OK:
            pass
        else:
            pass

    def _ev_click_on_treelist(self, event):

        self.curTreeItem = self.treeListCtrl.GetItemText(event.GetItem())

        if not self.curTreeItem:
            # 当前选中的TreeItemId对象操作

            MessageDialog("当前点击:{0}!".format(self.curTreeItem))
            for m_key, m_val in self.treeListCtrl.colleges.items():
                for s_key in m_val:
                    if s_key.get("名称", "") == self.curTreeItem:
                        if s_key.get("函数", "") != "未定义":
                            if (m_key == "衍生指标") or (m_key == "K线形态"):
                                # 第一步:收集控件中设置的选项
                                st_label = s_key["标识"]
                                st_code = self.init_code_input.GetValue()
                                st_name = self.code_table.get_name(st_code)

                                # 第二步:获取股票数据-使用self.stock_dat存储数据
                                if self.stock_dat.empty:
                                    MessageDialog("获取股票数据出错！\n")
                            else:
                                MessageDialog("该接口未定义！")
                                # self.function = getattr(
                                #     Base_Strategy_Group, s_key.get("define", "")
                                # )
                        else:
                            MessageDialog("该接口未定义！")
                        break

    def _init_treelist_ctrl(self, subpanel):

        # 创建一个 treeListCtrl object
        self.treeListCtrl = CollegeTreeListCtrl(
            parent=subpanel, pos=(-1, 39), size=(250, 200)
        )
        self.treeListCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self._ev_click_on_treelist)

        return self.treeListCtrl

    def _init_nav_notebook(self):

        # 创建参数区面板
        self.NavNoteb = wx.Notebook(self)

        self.NavNoteb.AddPage(self._init_treelist_ctrl(self.NavNoteb), "策略导航")
        self.NavNoteb.AddPage(self._init_grid_pl(self.NavNoteb), "股票池索引")

        return self.NavNoteb

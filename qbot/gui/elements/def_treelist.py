#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import wx
import wx.adv
import wx.gizmos
import wx.grid
import wx.html2


class CollegeTreeListCtrl(wx.gizmos.TreeListCtrl):

    colleges = {
        "经典策略": [
            {
                "名称": "N日突破",
                "标识": "趋势",
                "函数": "已定义",
                "define": "get_ndays_signal",
            },
            {
                "名称": "ATR止盈止损",
                "标识": "趋势",
                "函数": "已定义",
                "define": "get_ndays_atr_signal",
            },
        ],
        "自定义策略": [
            {"名称": "yx-zl-1", "标识": "综合", "函数": "未定义"},
            {"名称": "yx-zl-2", "标识": "趋势", "函数": "未定义"},
            {"名称": "yx-zl-3", "标识": "波动", "函数": "未定义"},
        ],
        "衍生指标": [
            {"名称": "均线交叉", "标识": "cross", "函数": "已定义"},
            {"名称": "跳空缺口", "标识": "jump", "函数": "已定义"},
            {"名称": "黄金分割", "标识": "fibonacci", "函数": "已定义"},
        ],
        "K线形态": [
            {"名称": "乌云盖顶", "标识": "CDLDARKCLOUDCOVER", "函数": "已定义"},
            {"名称": "三只乌鸦", "标识": "CDL3BLACKCROWS", "函数": "已定义"},
            {"名称": "十字星", "标识": "CDLDOJISTAR", "函数": "已定义"},
            {"名称": "锤头", "标识": "CDLHAMMER", "函数": "已定义"},
            {"名称": "射击之星", "标识": "CDLSHOOTINGSTAR", "函数": "已定义"},
        ],
    }

    def __init__(
        self,
        parent=None,
        id=-1,
        pos=(0, 0),
        size=wx.DefaultSize,
        style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT,
    ):

        wx.gizmos.TreeListCtrl.__init__(self, parent, id, pos, size, style)

        self.root = None
        self.InitUI()
        self.refDataShow(self.colleges)

    def InitUI(self):
        self.il = wx.ImageList(16, 16, True)
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
        self.il.Add(
            wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16))
        )
        self.SetImageList(self.il)
        self.AddColumn("名称")
        self.AddColumn("函数")
        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 100)

    def refDataShow(self, newDatas):
        # if self.root is not None:
        #    self.DeleteAllItems()

        if newDatas is not None:
            self.root = self.AddRoot("择时策略")
            self.SetItemText(self.root, "", 1)  # 第1列上添加

            for cityID in newDatas.keys():  # 填充整个树
                child = self.AppendItem(self.root, cityID)
                lastList = newDatas.get(cityID, [])
                self.SetItemText(child, cityID + " (共" + str(len(lastList)) + "个)", 0)
                self.SetItemImage(
                    child, 0, which=wx.TreeItemIcon_Normal
                )  # wx.TreeItemIcon_Expanded

                for index in range(len(lastList)):
                    college = lastList[index]  # TreeItemData是每一个ChildItem的唯一标示
                    # 以便在点击事件中获得点击项的位置信息
                    # "The TreeItemData class no longer exists, just pass your object directly to the tree instead
                    # data = wx.TreeItemData(cityID + "|" + str(index))
                    last = self.AppendItem(
                        child, str(index), data=cityID + "|" + str(index)
                    )
                    self.SetItemText(last, college.get("名称", ""), 0)
                    self.SetItemText(last, str(college.get("函数", "")), 1)
                    self.SetItemImage(
                        last, 0, which=wx.TreeItemIcon_Normal
                    )  # wx.TreeItemIcon_Expanded
                    self.Expand(self.root)

#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import wx
import wx.grid


class GridTable(wx.grid.Grid):

    def __init__(self, parent=None, nrow=30, ncol=20):

        wx.grid.Grid.__init__(self, parent, id=-1)
        self.CreateGrid(nrow, ncol)

    def AutoRowNums(self, cur_rows=0, to_rows=0):

        if cur_rows < to_rows:
            self.InsertRows(to_rows, to_rows - cur_rows, updateLabels=True)
        elif cur_rows > to_rows:
            self.DeleteRows(to_rows, cur_rows - to_rows, updateLabels=True)
        else:
            pass

    def AutoColNums(self, cur_cols=0, to_cols=0):

        if cur_cols < to_cols:
            self.InsertCols(cur_cols, to_cols - cur_cols, updateLabels=True)
        elif cur_cols > to_cols:
            self.DeleteCols(to_cols, cur_cols - to_cols, updateLabels=True)
        else:
            pass

    def DeleteAllRows(self):

        if self.GetNumberRows() > 0:
            self.DeleteRows(0, self.GetNumberRows(), updateLabels=True)

    def SetSelectCol(self, col_label):

        m = self.list_columns.index(col_label)
        self.SelectCol(m, addToSelected=False)

    def SetTable(self, data, tran_col):

        if isinstance(data, dict):
            # 字典类型 仅支持2列 key&value
            self.DeleteAllRows()
            for i, element in enumerate(tran_col):
                self.SetColLabelValue(i, element)

            id = 0
            for m_k, m_v in data.items():
                st_name_code_dict = m_v
                for s_k, s_v in st_name_code_dict.items():
                    self.InsertRows(id, 2)
                    self.SetCellValue(id, 0, s_k)
                    self.SetCellValue(id, 1, s_v)
                    id = id + 1
        else:
            # dataframe 类型
            df_data = data
            # try:
            if not df_data.empty:

                self.ClearGrid()
                self.list_columns = df_data.columns.tolist()

                self.AutoRowNums(self.GetNumberRows(), df_data.shape[0])
                self.AutoColNums(self.GetNumberCols(), df_data.shape[1])

                for col, series in df_data.iteritems():

                    m = self.list_columns.index(col)
                    if col in tran_col:
                        self.SetColLabelValue(m, tran_col.get(col, ""))
                    else:
                        self.SetColLabelValue(m, col)

                    for n, val in enumerate(series):
                        self.SetCellValue(n, m, str(val))

                    self.AutoSizeColumn(m, True)  # 自动调整列尺寸
            # except:
            # print("set df grid table error")

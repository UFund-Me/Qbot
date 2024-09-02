#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import os

import pandas as pd

QBOT_TOP_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)


class Base_File_Oper:
    rel_path = QBOT_TOP_PATH + "/qbot/common/configs/"

    @staticmethod
    def load_sys_para(filename, filepath=None):
        if filepath is None:
            filepath = Base_File_Oper.rel_path
        with open(filepath + filename, "r", encoding="utf-8") as load_f:
            para_dict = json.load(load_f)
        return para_dict

    @staticmethod
    def save_sys_para(filename, para_dict):
        with open(Base_File_Oper.rel_path + filename, "w", encoding="utf-8") as save_f:
            json.dump(para_dict, save_f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_tushare_basic():
        # 加载tushare basic接口的本地数据
        df_basic = pd.read_csv(
            Base_File_Oper.rel_path + "tushare_basic_info.csv",
            parse_dates=True,
            index_col=0,
            encoding="GBK",
        )
        return df_basic

    @staticmethod
    def save_tushare_basic(df_basic):
        # 存储tushare basic接口的本地数据
        df_basic.to_csv(
            Base_File_Oper.rel_path + "tushare_basic_info.csv",
            columns=df_basic.columns,
            index=True,
            encoding="GBK",
        )

    @staticmethod
    def read_tushare_token():
        # 设置token
        with open(Base_File_Oper.rel_path + "token.txt", "r", encoding="utf-8") as f:
            token = f.read()  # 读取你的token
        return token

    @staticmethod
    def save_patten_analysis(df_basic, filename):
        # 存储形态识别分析结果
        df_basic.to_csv(
            Base_File_Oper.rel_path + filename + ".csv",
            columns=df_basic.columns,
            index=True,
            encoding="GBK",
        )

    @staticmethod
    def read_log_trade(log_txt="logtrade.txt"):
        with open(Base_File_Oper.rel_path + log_txt, "r", encoding="gbk") as f:
            info = f.read()
        return info

    @staticmethod
    def txt2html(txt_file, html_file):
        # 读取TXT文件内容
        with open(txt_file, "r", encoding="utf-8") as file:
            txt_content = file.read()

        txt_content = []
        with open(txt_file, "r", encoding="utf-8") as file:
            for line in file:
                txt_content.append(line.strip())
                # print(line.strip())

        txt_content = "<br>".join(txt_content)
        # 创建HTML内容
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Converted from TXT</title>
        </head>
        <body>
            <p>{txt_content}</p>
        </body>
        </html>
        """

        # 将HTML内容写入文件
        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        # 打印消息
        print(f"TXT file '{txt_file}' has been converted to HTML file '{html_file}'.")


if __name__ == "__main__":

    Base_File_Oper.txt2html("test.log", "test1.html")

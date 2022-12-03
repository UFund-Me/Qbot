#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************

import datetime
import json
import os
import re
import sys

import pandas as pd
import requests

URL_PATTERN = '<a href="(.*?)".*?国务院办公厅关于%s年部分'
STATUTORY_HOLIDAY_TEXT_PATTERN = '<p align=.*?bold;">.*?、(.*?)：</span>(.*?)</p>'
Y_M_D_BETWEEN_PATTERN = r"(\d{4})年(\d{1,2})月(\d{1,2})日至(\d{4})年(\d{1,2})月(\d{1,2})日"
Y_M_D_PATTERN = r"(\d{4})年(\d{1,2})月(\d{1,2})日"
M_D_BETWEEN_PATTERN = r"(\d{1,2})月(\d{1,2})日至(\d{1,2})月(\d{1,2})日"
M_D_BETWEEN_PATTERN2 = r"(\d{1,2})月(\d{1,2})日至(\d{1,2})日"
M_D_PATTERN = r"(\d{1,2})月(\d{1,2})日"

TOP_DIR = sys.path[0] + "/.."
STATUTORY_HOLIDAY_PATH = TOP_DIR + "/config/"
GOV_OPEN_INFO_URL = (
    r"http://sousuo.gov.cn/s.htm?t=zhengce&q=%E8%8A%82%E5%81%87%E6%97%A5%E5%AE%89%E6%8E%92%E9%80%"
    r"9A%E7%9F%A5&timetype=&mintime=&maxtime=&sort=&sortType=&searchfield=&pcodeJiguan=&childtype="
    r"&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p=&n=&inpro=&sug_t="
)

CHINA_STATUTORY_HOLIDAY = ["元旦", "春节", "清明节", "劳动节", "端午节", "中秋节", "国庆节"]


def get_statutory_holiday_info_url():
    YEAR = str(datetime.datetime.now().year)
    response = requests.get(url=GOV_OPEN_INFO_URL)
    text = response.text

    result = re.findall(URL_PATTERN % YEAR, text, re.M)
    if result:
        return result[0]

    raise ValueError("Cannot get statutory holiday info url")


def get_date_info(text):
    "2018年123月30日至2019年1月1日放假调休"
    "2月4日至10日"
    "10月1日至7日放假调休"
    "4月4日放假，与周末连休"
    "1月27日至2月2日"
    date_info = {}
    YEAR = str(datetime.datetime.now().year)

    result = re.search(Y_M_D_BETWEEN_PATTERN, text)
    if result:
        start_year = result[1]
        start_month = result[2] if len(result[2]) == 2 else f"0{result[2]}"
        start_day = result[3] if len(result[3]) == 2 else f"0{result[3]}"
        date_info["start_date"] = "-".join([start_year, start_month, start_day])

        end_year = result[4]
        end_month = result[5] if len(result[5]) == 2 else f"0{result[5]}"
        end_day = result[6] if len(result[6]) == 2 else f"0{result[6]}"
        date_info["end_date"] = "-".join([end_year, end_month, end_day])

        return date_info

    result = re.search(M_D_BETWEEN_PATTERN, text)
    if result:
        start_year = YEAR
        start_month = result[1] if len(result[1]) == 2 else f"0{result[1]}"
        start_day = result[2] if len(result[2]) == 2 else f"0{result[2]}"
        date_info["start_date"] = "-".join([start_year, start_month, start_day])

        end_year = YEAR
        end_month = result[3] if len(result[3]) == 2 else f"0{result[3]}"
        end_day = result[4] if len(result[4]) == 2 else f"0{result[4]}"
        date_info["end_date"] = "-".join([end_year, end_month, end_day])
        return date_info

    result = re.search(M_D_BETWEEN_PATTERN2, text)
    if result:
        start_year = YEAR
        start_month = result[1] if len(result[1]) == 2 else f"0{result[1]}"
        start_day = result[2] if len(result[2]) == 2 else f"0{result[2]}"
        date_info["start_date"] = "-".join([start_year, start_month, start_day])

        end_year = YEAR
        end_month = start_month
        end_day = result[3] if len(result[3]) == 2 else f"0{result[3]}"
        date_info["end_date"] = "-".join([end_year, end_month, end_day])
        return date_info

    result = re.search(Y_M_D_PATTERN, text)
    if result:
        start_year = result[1]
        start_month = result[2] if len(result[2]) == 2 else f"0{result[2]}"
        start_day = result[3] if len(result[3]) == 2 else f"0{result[3]}"
        date_info["end_date"] = date_info["start_date"] = "-".join(
            [start_year, start_month, start_day]
        )
        return date_info

    result = re.search(M_D_PATTERN, text)
    if result:
        start_year = YEAR
        start_month = result[1] if len(result[1]) == 2 else f"0{result[1]}"
        start_day = result[2] if len(result[2]) == 2 else f"0{result[2]}"
        date_info["end_date"] = date_info["start_date"] = "-".join(
            [start_year, start_month, start_day]
        )
        return date_info
    raise ValueError("statutory holiday info Error")


def get_statutory_holiday_info():
    statutory_holiday_info = {}
    response = requests.get(url=get_statutory_holiday_info_url())
    text = response.content.decode("utf8")

    result = re.findall(STATUTORY_HOLIDAY_TEXT_PATTERN, text, re.M)

    for info in result:
        holiday_name_info = info[0]
        holiday_name = [
            holiday
            for holiday in CHINA_STATUTORY_HOLIDAY
            if holiday == holiday_name_info
        ]
        if holiday_name:
            statutory_holiday_info[holiday_name[0]] = get_date_info(
                info[1].split("。")[0]
            )
        else:
            holiday_name = [
                holiday_name_info
                for holiday in CHINA_STATUTORY_HOLIDAY
                if holiday in holiday_name_info
            ]
            statutory_holiday_info[holiday_name[0]] = get_date_info(
                info[1].split("。")[0]
            )
    return statutory_holiday_info


def statutory_holiday_info_to_csv():
    YEAR = str(datetime.datetime.now().year)
    statutory_holiday_info = get_statutory_holiday_info()
    statutory_holiday = []
    for name, info in statutory_holiday_info.items():
        statutory_holiday.append(
            {
                "name": name,
                "startDate": info["start_date"][-5:],
                "endDate": info["end_date"][-5:],
                "year": YEAR,
            }
        )
    df = pd.DataFrame(statutory_holiday)
    df.to_csv(STATUTORY_HOLIDAY_PATH + "national_holidays.csv", encoding="utf8")


def get_statutory_holiday():
    year = datetime.datetime.now().year
    df = pd.read_csv(STATUTORY_HOLIDAY_PATH + "national_holidays.csv", encoding="utf8")

    df = df.loc[df["year"] == year]
    if df.empty:
        statutory_holiday_info_to_csv()

    df = pd.read_csv(STATUTORY_HOLIDAY_PATH + "national_holidays.csv", encoding="utf8")
    data = pd.DataFrame(df, columns=["name", "startDate", "endDate"]).to_dict(
        orient="records"
    )
    response = json.dumps(data, indent=4, ensure_ascii=False)
    return response


if __name__ == "__main__":
    holidays_dir = TOP_DIR + "/config/national_holidays.csv"
    if os.path.exists(holidays_dir):
        get_statutory_holiday()
    else:
        statutory_holiday_info_to_csv()

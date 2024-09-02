import json
import os
import re


def extract_content(text):
    pattern = r"\((.*?)\)"  # 匹配()之间的内容
    result = re.findall(pattern, text)
    return result


def save_strings_as_json(str_data, file_path):
    data = json.loads(str_data)
    json_str = json.dumps(data)

    with open(file_path, "w") as file:
        file.write(json_str)


def file2dict(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_files_in_directory(path, file_suffix=[".csv"]):
    files_list = []
    for root, dirs, files in os.walk(path):
        for file_suf in file_suffix:
            for file in files:
                files_list.append(file.strip(file_suf))
    return files_list


# data_str="""
#         {
#             'universe': ['000300.SH', '000905.SH', '399006.SZ', 'SPX'],
#             'benchmarks': ['000300.SH'],
#             'factors': [
#                 ('rate', '$close/Ref($close,1) -1'),
#                 ('mom_20', '$close/Ref($close,20) -1'),
#                 ('buy_1', '$mom_20>0.08'),
#                 ('sell_1', '$mom_20<0')
#             ],
#             'factors_date': [('rank', '$mom_20')],
#             'buy': (['buy_1'], 1),
#             'sell': (['sell_1'], 1),
#             'order_by': ('rank', 2)  # 从大到小, 取前2
#         }
#         """
# save_strings_as_json(data_str, "data.txt")

"""
Author: Charmve yidazhang1@gmail.com
Date: 2023-06-02 22:04:52
LastEditors: Charmve yidazhang1@gmail.com
LastEditTime: 2023-06-02 22:05:42
FilePath: /newbasic/easytrader_example/easytrader_example.py
Version: 1.0.1
Blogs: charmve.blog.csdn.net
GitHub: https://github.com/Charmve
Description:

Copyright (c) 2023 by Charmve, All Rights Reserved.
Licensed under the MIT License.
"""

import easytrader


# 定义一个网格交易策略类
class GridTradeStrategy:
    def __init__(self, user, symbol, grid_num, grid_width):
        self.user = user  # easytrader客户端对象
        self.symbol = symbol  # 要交易的股票代码
        self.grid_num = grid_num  # 网格数量
        self.grid_width = grid_width  # 每个网格的宽度（百分比）
        self.init_price = user.get_price(symbol)  # 初始价格

    def execute(self):
        price = self.user.get_price(self.symbol)
        grid_price = [
            self.init_price * (1 + self.grid_width * i) for i in range(self.grid_num)
        ] + [self.init_price * (1 - self.grid_width * i) for i in range(self.grid_num)]
        grid_price.sort()

        for i in range(self.grid_num * 2):
            if (
                price > grid_price[i]
                and self.user.position[self.symbol]["sellable"] > 0
            ):
                self.user.sell(stock_code=self.symbol, price=price, amount=100)
                self.init_price = grid_price[i]
                break
            elif price < grid_price[i] and self.user.cash_available // price >= 100:
                self.user.buy(stock_code=self.symbol, price=price, amount=100)
                self.init_price = grid_price[i]
                break


# 登录华泰证券客户端
user = easytrader.use("ht_client")
user.prepare("华泰", username="your_username", password="your_password")

# 创建网格交易策略对象并执行交易
symbol = "600000"  # 要交易的股票代码
grid_num = 10  # 网格数量
grid_width = 0.01  # 每个网格的宽度（百分比）
strategy = GridTradeStrategy(user, symbol, grid_num, grid_width)

while True:
    strategy.execute()

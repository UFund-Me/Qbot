# !/usr/bin/env python3
# coding:utf-8

# larkbot.py

import base64
import hashlib
import hmac
from datetime import datetime

import requests

WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/efe3d146-84c4-4d84-aba9-3c4d1d9e4f1a"

# 发送更加个性化的消息 
# https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN#383d6e48
content_json = {
    "msg_type": "interactive",
    "timestamp": "timestamp",
    "sign": "sign",
    "card": {
        "elements": [{
                "tag": "div",
                "text": {
                        "content": "**西湖**，位于浙江省杭州市西湖区龙井路1号，杭州市区西部，景区总面积49平方千米，汇水面积为21.22平方千米，湖面面积为6.38平方千米。",
                        "tag": "lark_md"
                }
        }, {
                "actions": [{
                        "tag": "button",
                        "text": {
                                "content": "更多景点介绍 :玫瑰:",
                                "tag": "lark_md"
                        },
                        "url": "https://www.example.com",
                        "type": "default",
                        "value": {}
                }],
                "tag": "action"
        }],
        "header": {
                "title": {
                        "content": "今日旅游推荐",
                        "tag": "plain_text"
                }
        }
    }
}

class LarkBot:
    def __init__(self, secret: str) -> None:
        if not secret:
            raise ValueError("invalid secret key")
        self.secret = secret

    def gen_sign(self, timestamp: int) -> str:
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return sign

    def send(self, content: str) -> None:
        timestamp = int(datetime.now().timestamp())
        sign = self.gen_sign(timestamp)

        params = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "text",
            "content": {"text": content},
        }
        resp = requests.post(url=WEBHOOK_URL, json=params)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") and result["code"] != 0:
            print(result["msg"])
            return
        print("消息发送成功")

def main():
    WEBHOOK_SECRET = "wNMVU3ewSm2F0G2TwTX4Fd"
    bot = LarkBot(secret=WEBHOOK_SECRET)
    bot.send(content="[测试] 我是一只高级鸽子！")

if __name__ == '__main__':
    main()

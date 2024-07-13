#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Description: Send email unit test
#  How to use: python -m unittest -v send_email_test.TestSendEmail
#
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************


import datetime
import os
import sys
import unittest
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from pathlib import Path

TOP_DIR = Path(__file__).parent.parent.joinpath("utils")
sys.path.append(TOP_DIR)

from utils.send_email import send_email


class TestSendEmail(unittest.TestCase):
    SRC_DIR = Path(__file__).parent.parent.joinpath("qbot/gui")

    # 发件人邮箱
    mail_sender = "1144262839@qq.com"
    # 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
    mail_license = os.getenv("MAIL_LICENSE")
    # 收件人邮箱，可以为多个收件人
    mail_receivers = ["yidazhang1@gmail.com", "zhangwei@qcraft.ai"]
    # 邮件主题
    subject = """Python邮件测试"""

    def test_sendtext(self, mail_sender=mail_sender, mail_receivers=mail_receivers):
        # 邮件正文内容
        body_content = """你好，这是一个测试邮件!"""
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, "plain", "utf-8")
        self.assertTrue(send_email(mail_sender, mail_receivers, message_text))

    def test_sendattachment(self):
        # 构造附件
        attachment = MIMEText(
            open(self.SRC_DIR.joinpath("bkt_result/bkt_result.html"), "rb").read(),
            "base64",
            "utf-8",
        )
        # 设置附件信息
        attachment["Content-Disposition"] = 'attachment; filename="bkt_result.html"'
        self.assertTrue(send_email(self.mail_sender, self.mail_receivers, attachment))

    def test_sendimage(self):
        # 二进制读取图片
        image_data = open(self.SRC_DIR.joinpath("imgs/UFund.png"), "rb")
        # 设置读取获取的二进制数据
        message_image = MIMEImage(image_data.read())
        # 关闭刚才打开的文件
        image_data.close()
        self.assertTrue(send_email(self.mail_sender, self.mail_receivers, message_image))

    def test_sendhtml(self):
        # 发送 html 格式的邮件
        now_time = datetime.datetime.now()
        year = now_time.year
        month = now_time.month
        day = now_time.day
        mytime = str(year) + " 年 " + str(month) + " 月 " + str(day) + " 日 "
        fayanren = "爱因斯坦"
        zhuchiren = "牛顿"

        # 构造HTML
        html_content = """
                        <html>
                        <body>
                            <h1 align="center">这个是标题，xxxx通知</h1>
                            <p><strong>您好：</strong></p>
                            <blockquote><p><strong>以下内容是本次会议的纪要,请查收！</strong></p></blockquote>                    
                            <blockquote><p><strong>发言人：{fayanren}</strong></p></blockquote>
                            <blockquote><p><strong>主持人：{zhuchiren}</strong></p></blockquote>
                            <p align="right">{mytime}</p>
                        <body>
                        <html>
                        """.format(
            fayanren=fayanren, zhuchiren=zhuchiren, mytime=mytime
        )
        message_html = MIMEText(html_content, "html", "utf-8")
        self.assertTrue(send_email(self.mail_sender, self.mail_receivers, message_html))

    def test_qmail(self):
        self.assertTrue(self.test_sendtext())

    def test_gmail(self):
        self.assertTrue(self.test_sendtext())


if __name__ == "__main__":
    unittest.main()

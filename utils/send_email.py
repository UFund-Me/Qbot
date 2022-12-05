#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ****************************************************************************
#  Description: Send email unit test
#  How to use: python -m unittest -v test_send_semail.TestSendEmail
#
#  Copyright 2022 Charmve. All Rights Reserved.
#  Licensed under the MIT License.
# ****************************************************************************

import os
import smtplib
import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

TOP_DIR = Path(__file__).parent.parent.joinpath("gui")

# 发件人邮箱
mail_sender = "1144262839@qq.com"
# 邮箱授权码,注意这里不是邮箱密码,如何获取邮箱授权码,请看本文最后教程
mail_license = os.getenv("MAIL_LICENSE")
# 收件人邮箱，可以为多个收件人
mail_receivers = ["yidazhang1@gmail.com", "zhangwei@qcraft.ai"]
# 邮件主题
subject = """Python邮件测试"""

# 邮件正文内容
body_content = """你好，这是一个测试邮件!"""
# 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
message_text = MIMEText(body_content, "plain", "utf-8")

# 二进制读取图片
image_data = open(TOP_DIR.joinpath("imgs/UFund.png"), "rb")
# 设置读取获取的二进制数据
message_image = MIMEImage(image_data.read())
# 关闭刚才打开的文件
image_data.close()

# 构造附件
attachment = MIMEText(
    open(TOP_DIR.joinpath("bkt_result/bkt_result.html"), "rb").read(), "base64", "utf-8"
)
# 设置附件信息
attachment["Content-Disposition"] = 'attachment; filename="bkt_result.html"'

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


def send_email(mail_sender, mail_receivers, content):

    # 创建SMTP对象
    if "qq" in mail_sender:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    elif "gmail" in mail_sender:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Connect to the server
        server.starttls()
    elif "163" in mail_sender:
        server = smtplib.SMTP()
        # 设置发件人邮箱的域名和端口，端口地址为25
        server.connect("smtp.163.com", 25)
    else:
        print("Please check your sender email.")

    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    # server.set_debuglevel(1)

    # Connect and login to the email server
    server.login(mail_sender, mail_license)

    # Loop over each email to send to
    for mail_receiver in mail_receivers:
        # Setup MIMEMultipart for each email address (if we don't do this, the emails will concatenate on each email sent)
        msg = MIMEMultipart()
        msg["From"] = mail_sender
        msg["To"] = mail_receiver
        msg["Subject"] = subject

        print("Send to: ", mail_receiver)

        # # Attach the message to the MIMEMultipart object
        # msg.attach(message_text)
        # msg.attach(message_image)
        # # Attach the attachment file
        # msg.attach(attachment)
        msg.attach(content)

        # Send the email to this specific email address
        server.sendmail(mail_sender, mail_receiver, msg.as_string())
        print("邮件发送成功")
        return True

    # Quit the email server when everything is done
    server.quit()


if __name__ == "__main__":
    send_email(mail_sender, mail_receivers, message_text)
    # send_email(mail_sender, mail_receivers, message_image)
    # send_email(mail_sender, mail_receivers, attachment)
    # send_email(mail_sender, mail_receivers, message_html)

# -*- coding: utf-8 -*-
"""
module for realtime watch and notfication
"""
# deprecated
# 该模块与现在的主线进展关系不大，可用性不强，
# xalpha 不应过度干涉通知或可能的自动交易部分
# 因此该模块可能随时不再支持

import datetime as dt
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr
from re import match
import pandas as pd

from xalpha.cons import today_obj, rget
from xalpha.info import fundinfo
from xalpha.trade import trade


def _format_addr(s):
    """
    parse the email sender and receiver, Chinese encode and support

    :param s: eg. 'name <email@website.com>, name2 <email2@web2.com>'
    """
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def mail(
    title,
    content,
    sender=None,
    receiver=None,
    password=None,
    server=None,
    port=None,
    sender_name="sender",
    receiver_name=None,
):
    """
    send email

    :param title: str, title of the email
    :param content: str, content of the email, plain text only
    :param conf: all other paramters can be import as a dictionay, eg.conf = {'sender': 'aaa@bb.com',
        'sender_name':'name', 'receiver':['aaa@bb.com','ccc@dd.com'], 'password':'123456',
        'server':'smtp.bb.com','port':123, 'receiver_name':['me','guest']}.
        The receiver_name and sender_name options can be omitted.
    """
    ret = True
    try:
        if receiver_name is None:
            receiver_name = ["receiver" for _ in receiver]
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = _format_addr("%s <%s>" % (sender_name, sender))
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        receivestr = ""
        for i, s in enumerate(receiver):
            receivestr += receiver_name[i]
            receivestr += " <"
            receivestr += s
            receivestr += ">, "
        msg["To"] = _format_addr(receivestr)  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg["Subject"] = title  # 邮件的主题，即标题

        server = smtplib.SMTP_SSL(server, port)  # 发件人邮箱中的SMTP服务器和端口号
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(
            sender, receiver, msg.as_string()
        )  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
    except Exception:
        ret = False
    return ret


class rtdata:
    """
    get real time data of specific funds

    :param code: string of six digitals for funds
    """

    def __init__(self, code):
        url = "http://fundgz.1234567.com.cn/js/" + code + ".js"
        page = rget(url)
        self.code = code
        self.rtvalue = float(match(r'.*"gsz":"(\d*\.\d*)",.*', page.text)[1])
        self.name = match(r'.*"name":"([^,]*)",.*', page.text)[1]
        self.time = dt.datetime.strptime(
            match(r'.*"gztime":"([\d\s\-\:]*)".*', page.text)[1], "%Y-%m-%d %H:%M"
        )


def rfundinfo(
    code, round_label=0, dividend_label=0, fetch=False, save=False, path="", form="csv"
):
    """
    give a fundinfo object with todays estimate netvalue at running time

    :param code: string of six digitals for funds
    :param fetch: boolean, when open the fetch option, info class will try fetching from local files first in the init
    :param save: boolean, when open the save option, info classes automatically save the class to files
    :param path: string, the file path prefix of IO
    :param form: string, the format of IO, options including: 'csv'
    :returns: the fundinfo object
    """
    fundobj = fundinfo(
        code,
        round_label=round_label,
        dividend_label=dividend_label,
        fetch=fetch,
        save=save,
        path=path,
        form=form,
    )
    rt = rtdata(code)
    rtdate = dt.datetime.combine(rt.time, dt.time.min)
    rtvalue = rt.rtvalue
    if (rtdate - fundobj.price.iloc[-1].date).days > 0:
        fundobj.price = fundobj.price.append(
            pd.DataFrame(
                [[rtdate, rtvalue, fundobj.price.iloc[-1].totvalue, 0]],
                columns=["date", "netvalue", "totvalue", "comment"],
            ),
            ignore_index=True,
        )
    return fundobj


class review:
    """
    review policys and give the realtime purchase suggestions

    :param policylist: list of policy object
    :param namelist: list of names of corresponding policy, default as 0 to n-1
    :param date: object of datetime, check date, today is prefered, date other than is not guaranteed
    """

    def __init__(self, policylist, namelist=None, date=today_obj()):
        self.warn = []
        self.message = []
        self.policylist = policylist
        if namelist is None:
            self.namelist = [i for i in range(len(policylist))]
        else:
            self.namelist = namelist
        assert len(self.policylist) == len(self.namelist)
        for i, policy in enumerate(policylist):
            row = policy.status[policy.status["date"] == date]
            if len(row) == 1:
                warn = (
                    policy.aim.name,
                    policy.aim.code,
                    row.iloc[0].loc[policy.aim.code],
                    self.namelist[i],
                )
                self.warn.append(warn)
                if warn[2] > 0:
                    sug = "买入%s元" % warn[2]
                elif warn[2] < 0:
                    ratio = -warn[2] / 0.005 * 100
                    share = (
                        trade(fundinfo(warn[1]), policy.status)
                        .briefdailyreport()
                        .get("currentshare", 0)
                    )
                    share = -warn[2] / 0.005 * share
                    sug = "卖出%s%%的份额，也即%s份额" % (ratio, share)
                self.message.append(
                    "根据%s计划，建议%s，%s(%s)" % (warn[3], sug, warn[0], warn[1])
                )
        self.content = "\n".join(map(str, self.message))

    def __str__(self):
        return self.content

    def notification(self, conf):
        """
        send email of self.content, at least support for qq email sender

        :param conf: the configuration dictionary for email send settings, no ** before the dict in needed.
            eg.conf = {'sender': 'aaa@bb.com',
            'sender_name':'name', 'receiver':['aaa@bb.com','ccc@dd.com'], 'password':'123456',
            'server':'smtp.bb.com','port':123, 'receiver_name':['me','guest']}.
            The receiver_name and sender_name options can be omitted.
        """
        if self.content:
            ret = mail("Notification", self.content, **conf)
            if ret:
                print("邮件发送成功")
            else:
                print("邮件发送失败")
        else:
            print("没有提醒待发送")

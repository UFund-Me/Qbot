import logging
import smtplib

from arbitrage import config
from arbitrage.observers.observer import Observer


def send_email(subject, message):
    _to = config.smtp_to
    _from = config.smtp_from
    mime_message = (
        """From: Python Arbitrage Script <%(_from)s>
To: <%(_to)s>
Subject: %(subject)s

%(message)s
"""
        % locals()
    )
    try:
        smtpObj = smtplib.SMTP(config.smtp_host)
        smtpObj.sendmail(_from, [_to], mime_message)
    except smtplib.SMTPException:
        logging.warn("Unable to send email")


class Emailer(Observer):
    def opportunity(
        self,
        profit,
        volume,
        buyprice,
        kask,
        sellprice,
        kbid,
        perc,
        weighted_buyprice,
        weighted_sellprice,
    ):
        if profit > config.profit_thresh and perc > config.perc_thresh:
            message = """profit: %f USD with volume: %f BTC
buy at %.4f (%s) sell at %.4f (%s) ~%.2f%%
""" % (
                profit,
                volume,
                buyprice,
                kask,
                sellprice,
                kbid,
                perc,
            )
            send_email("Arbitrage Bot", message)

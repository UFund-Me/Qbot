import logging

from arbitrage import config
from arbitrage.observers.observer import Observer
from sleekxmpp import ClientXMPP

# from sleekxmpp.exceptions import IqError, IqTimeout


class MyXMPPClient(ClientXMPP):
    def __init__(self):
        logger = logging.getLogger("sleekxmpp")
        logger.setLevel(logging.ERROR)
        ClientXMPP.__init__(self, config.xmpp_jid, config.xmpp_password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.connect()
        self.process(block=False)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def msend_message(self, message):
        logging.debug('Sending XMPP message: "%s" to %s' % (message, config.xmpp_to))
        self.send_message(mto=config.xmpp_to, mbody=message, mtype="chat")

    def message(self, msg):
        # TODO: Use this to control / re-config
        pass  # msg.reply("%(body)s" % msg).send()


class XmppMessager(Observer):
    def __init__(self):
        self.xmppclient = MyXMPPClient()

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
            message = (
                "profit: %f USD with volume: %f BTC - buy at %.4f (%s) sell at %.4f (%s) ~%.2f%%"
                % (profit, volume, buyprice, kask, sellprice, kbid, perc)
            )
            self.xmppclient.msend_message(message)

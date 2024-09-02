# Copyright (C) 2013, Maxime Biais <maxime@biais.org>

import argparse
import glob
import inspect
import logging
import os
import sys

from arbitrage import public_markets
from arbitrage.arbitrer import Arbitrer


class ArbitrerCLI:
    def __init__(self):
        self.inject_verbose_info()

    def inject_verbose_info(self):
        logging.VERBOSE = 15
        logging.verbose = lambda x: logging.log(logging.VERBOSE, x)
        logging.addLevelName(logging.VERBOSE, "VERBOSE")

    def exec_command(self, args):
        if "watch" in args.command:
            self.create_arbitrer(args)
            self.arbitrer.loop()
        if "replay-history" in args.command:
            self.create_arbitrer(args)
            self.arbitrer.replay_history(args.replay_history)
        if "get-balance" in args.command:
            self.get_balance(args)
        if "list-public-markets" in args.command:
            self.list_markets()
        if "generate-config" in args.command:
            self.generate_sample_config()

    def get_market_list(self):
        markets = []
        for filename in glob.glob(os.path.join(public_markets.__path__[0], "*.py")):
            module_name = os.path.basename(filename).replace(".py", "")
            if not module_name.startswith("_"):
                module = __import__("arbitrage.public_markets." + module_name)
                test = eval("module.public_markets." + module_name)
                for name, obj in inspect.getmembers(test):
                    if inspect.isclass(obj) and "Market" in (
                        j.__name__ for j in obj.mro()[1:]
                    ):
                        if not obj.__module__.split(".")[-1].startswith("_"):
                            markets.append(obj.__name__)
        return markets

    def list_markets(self):
        markets = self.get_market_list()
        markets.sort()
        print("\n".join(markets))
        sys.exit(0)

    def generate_sample_config(self):
        markets = self.get_market_list()
        markets.sort()
        print("markets = [")
        print('",\n'.join(['  "' + i for i in markets]) + '"')
        print("]")
        print('observers = ["Logger"]')
        print(
            """
refresh_rate = 60
market_expiration_time = 120  # in seconds: 2 minutes

# SafeGuards
max_tx_volume = 1  # in BTC
min_tx_volume = 0.01  # in BTC
balance_margin = 0.05  # 5%
profit_thresh = 0  # in USD
perc_thresh = 0  # in %"""
        )
        sys.exit(0)

    def get_balance(self, args):
        if not args.markets:
            logging.error("You must use --markets argument to specify markets")
            sys.exit(2)
        pmarkets = args.markets.split(",")
        pmarketsi = []
        for pmarket in pmarkets:
            exec("import arbitrage.private_markets." + pmarket.lower())
            market = eval(
                "arbitrage.private_markets."
                + pmarket.lower()
                + ".Private"
                + pmarket
                + "()"
            )
            pmarketsi.append(market)
        for market in pmarketsi:
            print(market)

    def create_arbitrer(self, args):
        self.arbitrer = Arbitrer()
        if args.observers:
            self.arbitrer.init_observers(args.observers.split(","))
        if args.markets:
            self.arbitrer.init_markets(args.markets.split(","))

    def init_logger(self, args):
        level = logging.INFO
        if args.verbose:
            level = logging.VERBOSE
        if args.debug:
            level = logging.DEBUG
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s", level=level
        )

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-d", "--debug", help="debug verbose mode", action="store_true"
        )
        parser.add_argument(
            "-v", "--verbose", help="info verbose mode", action="store_true"
        )
        parser.add_argument(
            "-o", "--observers", type=str, help="observers, example: -oLogger,Emailer"
        )
        parser.add_argument(
            "-m",
            "--markets",
            type=str,
            help="markets, example: -m BitstampEUR,KrakenEUR",
        )
        parser.add_argument(
            "command",
            nargs="*",
            default="watch",
            help='verb: "watch|replay-history|get-balance|list-public-markets"',
        )
        args = parser.parse_args()
        self.init_logger(args)
        self.exec_command(args)


def main():
    cli = ArbitrerCLI()
    cli.main()


if __name__ == "__main__":
    main()

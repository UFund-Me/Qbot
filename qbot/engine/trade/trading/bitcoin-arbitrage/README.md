# bitcoin-arbitrage - opportunity detector and automated trading

It gets order books from supported exchanges and calculate arbitrage
opportunities between each markets. It takes market depth into account.

Currently supported exchanges to get data:

- Bitstamp (USD, EUR)
- Paymium (EUR)
- Bitfinex (USD, EUR)
- bitFlyer (USD, EUR)
- Kraken (USD, EUR)
- OkCoin (CNY)
- Gemini (USD)
- BTCC (CNY)
- GDAX (USD, EUR)
- CEX.io (USD, EUR)
- Binance (USD)

Currently supported exchanges to automate trade:

- Bitstamp (USD)
- Paymium (EUR)

## WARNING

**Real trading bots are included. Don't put your API keys in config.py
if you don't know what you are doing.**

## Installation And Configuration

```sh
cp arbitrage/config.py-example arbitrage/config.py
```

Then edit config.py file to setup your preferences: watched markets
and observers

You need Python3 to run this program. To install on Debian, Ubuntu, or
variants of them, use:

```sh
sudo apt-get install python3 python3-pip python-nose
```

To use the observer XMPPMessager you will need to install sleekxmpp:

```sh
pip3 install sleekxmpp
```

## Run

To run the opportunity watcher:

```sh
$ python3 -m arbitrage -v
2013-03-12 03:52:14,341 [INFO] profit: 30.539722 EUR with volume: 10 BTC - buy at 29.3410 (MtGoxEUR) sell at29.4670 (Bitcoin24EUR) ~10.41%
2013-03-12 03:52:14,356 [INFO] profit: 66.283642 EUR with volume: 10 BTC - buy at 29.3410 (MtGoxEUR) sell at30.0000 (PaymiumEUR) ~22.59%
2013-03-12 03:52:14,357 [INFO] profit: 31.811390 EUR with volume: 10 BTC - buy at 29.3410 (MtGoxEUR) sell at30.0000 (IntersangoEUR) ~10.84%
2013-03-12 03:52:45,090 [INFO] profit: 9.774324 EUR with volume: 10 BTC - buy at 35.3630 (Bitcoin24EUR) sellat 35.4300 (PaymiumEUR) ~2.76%
```

To check your balance on an exchange (also a good way to check your accounts configuration):

```sh
python3 -m arbitrage -m Paymium get-balance
python3 -m arbitrage -m Paymium,BitstampUSD get-balance
```

Run tests

```sh
nosetests arbitrage/
```

### Alternative usage

List supported public markets:

```sh
python3 -m arbitrage list-public-markets
```

Help:

```sh
python3 -m arbitrage -h
```

## TODO

- Tests
- Write documentation
- Add other exchanges:
  - icbit
- Update order books with a WebSocket client for supported exchanges
  (Kraken, Bitfinex, Paymium)
- Better history handling for observer "HistoryDumper" (Redis ?)
- Move EUR / USD from a market to an other:
  - Coupons
  - Ripple ?
  - Stable coins
  - Negative Operations
  - Add support for other cryptocurrencies and triangular arbitrage

## LICENSE

MIT

Copyright (c) 2013 Maxime Biais <firstname.lastname@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#!/usr/bin/env python

import sys

from setuptools import setup

if sys.version_info < (3,):
    print("bitcoin-arbitrage requires Python version >= 3.0")
    sys.exit(1)

setup(
    name="bitcoin-arbitrage",
    packages=["arbitrage"],
    version="0.1",
    description="Bitcoin arbitrage opportunity watcher",
    author="Maxime Biais",
    author_email="maxime.biais@gmail.com",
    url="https://github.com/maxme/bitcoin-arbitrage",
    arbitrage=["bin/bitcoin-arbitrage"],
    test_suite="nose.collector",
    tests_require=["nose"],
)

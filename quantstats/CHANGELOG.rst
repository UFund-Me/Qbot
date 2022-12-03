Change Log
===========

0.0.59
-----
- Fixed EOY compounded return calculation

0.0.58
-----
- Run fillna(0) on plot's beta (issue #193)

0.0.57
-----
- Fixed `sigma` calculation in `stats.probabilistic_ratio()`

0.0.56
-----
- Added option to explicitly provide the benchmark title via `benchmark_title=...`

0.0.55
-----
- Fix for benchmark name in html report when supplied by the user

0.0.54
------
- Fixed dependency name in requirements.txt


0.0.53
------
- Added information ratio to reports

0.0.52
------
- Added Treynor ratio

0.0.51
------
- Added max consecutive wins/losses to full report
- Added “correlation to benchmark” to report
- Cleanup inf/nan from reports
- Added benchmark name to stats column and html report
- Added probabilistic sharpe/sortino ratios
- Fix relative dates calculations

0.0.50
------
- Fixed a bug when reporting the max drawdown

0.0.49
------
- Fixed an issue with saving the HTML report as a file

0.0.48
------
- Fixed RF display bug

0.0.47
------
- Fixed average DD display bug

0.0.46
------
- Misc bug fixes and speedups

0.0.45
------
- Fixed ``stats.rolling_sharpe()`` parameter mismatch

0.0.44
------
- Match dates logic on ``utils.make_index()``

0.0.43
------
- Fixed ``stats.rolling_sortino()`` calculations
- Added ``match_dates`` flag to reports to make strategy and benchmark comparible by syncing their dates and frequency
- Added ``prepare_returns`` flag to ``utils._prepare_benchmark()``
- Misc code cleanup and speedups

0.0.42
------
- Usability improvements

0.0.41
------
- Typos fixed

0.0.40
------
- Added rebalance option to ``utils.make_index()``
- Added option to add ``log_scale=True/False` to ``plots.snapshot()``

0.0.39
------
- Fixed ``plots.rolling_volatility()`` benchmark display (bug introduced in 0.0.37)

0.0.38
------
- Added ``stats.smart_sharpe()`` and ``stats.smart_sortino()``

0.0.37
------
- added ``stats.rolling_sharpe()``, ``stats.rolling_sortino()``, ``stats.and rolling_volatility()``
- Added ``stats.distribution()``
- Added Omega ratio
- BREAKING CHANGE: Eenamed ``trading_year_days`` param to ``periods_per_year``
- Misc code cleanup and speedups

0.0.36
------
- Added ``as_pct`` params to ``reports.metrics()`` for when you need display data as DataFrame

0.0.35
------
- Passing correct rolling windows in ``rolling_beta()``
- Added Serenity Index
- Passing ``trading_year_days`` to method ``metrics``
- Fixed "day is out of range for month" error

0.0.34
------
- Fixed bug in ``stats.consecutive_wins()`` and ``stats.consecutive_losses()``
- Fixed seaborn's depreated ``distplot`` warning
- Improved annualization by passing ``trading_year_days``

0.0.33
------
- Added option to pass the number of days per year in reports, so you can now use ``trading_year_days=365`` if you're trading crypto, or any other number for intl. markets.

0.0.32
------
- Fixed bug in ``plot_histogram()`` (issues 94+95)

0.0.31
------
- Enable period setting for adjusted sortino
- Added ``utils.make_index()`` for easy "etf" creation

0.0.30
------
- Fixed PIP installer

0.0.29
------
- Minor code refactoring

0.0.28
------
- ``gain_to_pain`` renamed to ``gain_to_pain_ratio``
- Minor code refactoring

0.0.27
------
- Added Sortino/√2 and Gain/Pain ratio to report
- Merged PRs to fix some bugs

0.0.26
------
- Misc bug fixes and code improvements

0.0.25
------
- Fixed ``conditional_value_at_risk()``
- Fixed ``%matplotlib inline`` issue notebooks

0.0.24
------
- Added mtd/qtd/ytd methods for panda (usage: ``df.mtd()``)
- Fixed Pandas deprecation warning
- Fixed Matplotlib deprecation warning
- Try setting ``%matplotlib inline`` automatic in notebooks

0.0.23
------
- Fixed profit Factor formula

0.0.22
------
- Misc bug fixes

0.0.21
------
- Fixed chart EOY chart's ``xticks`` when charting data with 10+ years
- Fixed issue where daily return >= 100%
- Fixed Snapshot plot
- Removed duplicaated code
- Added conda installer
- Misc code refactoring and optimizations

0.0.20
------
- Misc bugfixes

0.0.19
------
- Cleaning up data before calculations (replaces inf/-inf/-0 with 0)
- Removed usage of ``pandas.compound()`` for future ``pandas`` version compatibility
- Auto conversion of price-to-returns and returns-to-data as needed

0.0.18
------
- Fixed issue when last date in data is in the past (issue #4)
- Fixed issue when data has less than 5 drawdown periods (issue #4)

0.0.17
------
- Fixed CAGR calculation for more accuracy
- Handles drawdowns better in live trading mode when currently in drawdown

0.0.16
------
- Handles no drawdowns better

0.0.15
------
- Better report formatting
- Code cleanup

0.0.14
------
- Fixed calculation for rolling sharpe and rolling sortino charts
- Nicer CSS when printing html reports

0.0.13
------
- Fixed non-compounded plots in reports when using ``compounded=False``

0.0.12
------
- Option to add ``compounded=True/False`` to reports (default is ``True``)

0.0.11
------
- Minor bug fixes

0.0.10
------
- Updated to install and use ``yfinance`` instead of ``fix_yahoo_finance``

0.0.09
------
- Added support for 3 modes (cumulative, compounded, fixed amount) in ``plots.earnings()`` and ``utils.make_portfolio()``
- Added two DataFrame utilities: ``df.curr_month()`` and ``df.date(date)``
- Misc bug fixes and code refactoring


0.0.08
------
- Better calculations for cagr, var, cvar, avg win/loss and payoff_ratio
- Removed unused param from ``to_plotly()``
- Added risk free param to ``log_returns()`` + renamed it to ``to_log_returns()``
- Misc bug fixes and code improvements

0.0.07
------
- Plots returns figure if ``show`` is set to False

0.0.06
------
- Minor bug fix

0.0.05
------
- Added ``plots.to_plotly()`` method
- Added Ulcer Index to metrics report
- Better returns/price detection
- Bug fixes and code refactoring

0.0.04
------
- Added ``pct_rank()`` method to stats
- Added ``multi_shift()`` method to utils

0.0.03
------
- Better VaR/cVaR calculation
- Fixed calculation of ``to_drawdown_series()``
- Changed VaR/cVaR default confidence to 95%
- Improved Sortino formula
- Fixed conversion of returns to prices (``to_prices()``)

0.0.02
------
- Initial release

0.0.01
------
- Pre-release placeholder

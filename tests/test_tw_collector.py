#!/usr/bin/python
# -*- coding: UTF-8 -*-

import importlib.util
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent.joinpath("qbot", "data")))
import tw_collector as tw  # noqa: E402

HAS_QLIB = importlib.util.find_spec("qlib") is not None


def make_raw(dates, start_price, seed, ex_div=None, dividend=0.0, suspended=()):
    """產生和 tw_collector.fetch_yahoo 同格式的原始日線。"""
    rng = np.random.default_rng(seed)
    close = start_price * np.cumprod(1 + rng.normal(0, 0.01, len(dates)))
    adjclose = close.copy()
    if ex_div is not None:
        pos = dates.get_loc(pd.Timestamp(ex_div))
        close[pos:] -= dividend
        # Yahoo 的還原價：除息日前的價格乘上 (1 - 股息 / 除息前一日收盤)
        adjclose = close.copy()
        adjclose[:pos] *= 1 - dividend / close[pos - 1]
    volume = rng.integers(1_000_000, 5_000_000, len(dates)).astype(float)
    df = pd.DataFrame(
        {
            "date": dates,
            "open": close * 0.995,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "adjclose": adjclose,
            "volume": volume,
            "dividends": 0.0,
            "stock_splits": 0.0,
        }
    )
    for day in suspended:
        df.loc[df["date"] == pd.Timestamp(day), "volume"] = 0
    return df


class StockListTest(unittest.TestCase):
    def test_filter_stock_info(self):
        info = pd.DataFrame(
            {
                "industry_category": [
                    "半導體業",
                    "ETF",
                    "電子零組件業",
                    "半導體業",
                    "其他",
                ],
                "stock_id": ["2330", "0050", "6488", "2330", "7777"],
                "stock_name": ["台積電", "元大台灣50", "環球晶", "台積電", "興櫃股"],
                "type": ["twse", "twse", "tpex", "twse", "emerging"],
                "date": ["2026-10-01"] * 5,
            }
        )
        df = tw.filter_stock_info(info)
        self.assertEqual(df["symbol"].tolist(), ["TW2330", "TW6488"])
        self.assertEqual(df["yahoo"].tolist(), ["2330.TW", "6488.TWO"])
        self.assertEqual(df["market"].tolist(), ["twse", "tpex"])

    def test_load_symbols_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp, "list.txt")
            path.write_text(
                "# 範例\n2330 台積電\n6488.two\n\n2317.TW  # 鴻海\n2330\n",
                encoding="utf-8",
            )
            df = tw.load_symbols_file(path)
            self.assertEqual(df["symbol"].tolist(), ["TW2330", "TW6488", "TW2317"])
            self.assertEqual(df["yahoo"].tolist(), ["2330.TW", "6488.TWO", "2317.TW"])
            self.assertEqual(df["name"].tolist()[0], "台積電")

            path.write_text("0050\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                tw.load_symbols_file(path)


class FetchYahooTest(unittest.TestCase):
    def test_columns_and_timezone(self):
        index = pd.DatetimeIndex(
            ["2024-01-02", "2024-01-03"], tz="Asia/Taipei", name="Date"
        )
        history = pd.DataFrame(
            {
                "Open": [590.0, 584.0],
                "High": [593.0, 585.0],
                "Low": [589.0, 576.0],
                "Close": [593.0, 578.0],
                "Adj Close": [570.1, 555.7],
                "Volume": [26059058, 37106763],
                "Dividends": [0.0, 0.0],
                "Stock Splits": [0.0, 0.0],
            },
            index=index,
        )
        ticker = mock.Mock()
        ticker.history.return_value = history
        fake_yf = types.SimpleNamespace(Ticker=mock.Mock(return_value=ticker))
        with mock.patch.dict(sys.modules, {"yfinance": fake_yf}):
            df = tw.fetch_yahoo("2330.TW", "2024-01-01", "2024-01-04")
        fake_yf.Ticker.assert_called_once_with("2330.TW")
        self.assertEqual(ticker.history.call_args.kwargs["auto_adjust"], False)
        self.assertEqual(
            df.columns.tolist(), ["date"] + list(tw.YAHOO_COLUMNS.values())
        )
        self.assertEqual(
            df["date"].tolist(), list(pd.to_datetime(["2024-01-02", "2024-01-03"]))
        )
        self.assertIsNone(df["date"].dt.tz)


class NormalizeTest(unittest.TestCase):
    def setUp(self):
        self.dates = pd.bdate_range("2024-01-01", periods=30)
        self.raw = make_raw(
            self.dates,
            100.0,
            seed=1,
            ex_div=self.dates[10],
            dividend=3.0,
            suspended=[self.dates[20]],
        )

    def test_adjustment_is_reversible(self):
        df = tw.normalize_symbol(self.raw, "TW2330", self.dates).set_index("date")
        raw = self.raw.set_index("date")
        valid = raw["volume"] > 0
        # qlib 用 close / factor 換回實際股價，用 volume * factor 換回實際股數
        np.testing.assert_allclose(
            (df["close"] / df["factor"])[valid], raw["close"][valid]
        )
        np.testing.assert_allclose(
            (df["volume"] * df["factor"])[valid], raw["volume"][valid]
        )
        self.assertAlmostEqual(df["close"].dropna().iloc[0], 1.0)

    def test_change_ignores_dividend_and_suspension(self):
        df = tw.normalize_symbol(self.raw, "TW2330", self.dates).set_index("date")
        raw = self.raw.set_index("date")
        ex_div = self.dates[10]
        expected = raw.loc[ex_div, "adjclose"] / raw["adjclose"].shift(1)[ex_div] - 1
        self.assertAlmostEqual(df.loc[ex_div, "change"], expected)
        self.assertGreater(df.loc[ex_div, "change"], -0.05)

        suspended = self.dates[20]
        self.assertTrue(df.loc[suspended, ["close", "volume", "change"]].isna().all())
        # 復牌日的 change 對比停牌前最後一個收盤價
        resumed = self.dates[21]
        expected = df.loc[resumed, "close"] / df.loc[self.dates[19], "close"] - 1
        self.assertAlmostEqual(df.loc[resumed, "change"], expected)

    def test_vwap_and_calendar_alignment(self):
        calendar = self.dates.delete(5)
        raw = self.raw.drop(index=7)
        df = tw.normalize_symbol(raw, "TW2330", calendar).set_index("date")
        self.assertNotIn(self.dates[5], df.index)
        self.assertTrue(np.isnan(df.loc[self.dates[7], "close"]))
        np.testing.assert_allclose(
            df["vwap"].dropna(), ((df["high"] + df["low"] + df["close"]) / 3).dropna()
        )

    def test_index_keeps_zero_volume_rows(self):
        raw = self.raw.assign(volume=0.0, adjclose=self.raw["close"])
        df = tw.normalize_symbol(raw, "TWII", self.dates, is_index=True)
        self.assertEqual(df["close"].notna().sum(), len(self.dates))
        self.assertEqual(df["factor"].nunique(), 1)


class UniverseTest(unittest.TestCase):
    def test_quarterly_top_n_without_lookahead(self):
        dates = pd.bdate_range("2020-01-01", "2020-12-31")
        values = pd.DataFrame(index=dates)
        values["A"] = 100.0
        values["B"] = np.where(dates <= "2020-06-30", 90.0, 0.0)
        values["C"] = np.where(dates < "2020-08-14", 10.0, 1000.0)
        values["D"] = 50.0
        df = tw.compute_liquidity_universe(values, top_n=2, window=20, freq="Q")
        spans = {
            s: g[["start", "end"]].values.tolist() for s, g in df.groupby("symbol")
        }
        self.assertEqual(spans["A"], [["2020-04-01", "2020-12-31"]])
        self.assertEqual(spans["B"], [["2020-04-01", "2020-09-30"]])
        # C 在 8 月中就放量，但要等 9/30 重選後才入選
        self.assertEqual(spans["C"], [["2020-10-01", "2020-12-31"]])
        self.assertNotIn("D", spans)

    def test_unlisted_stock_waits_for_full_window(self):
        dates = pd.bdate_range("2020-01-01", "2020-06-30")
        values = pd.DataFrame(index=dates)
        values["A"] = 1.0
        values["NEW"] = np.where(dates >= "2020-03-20", 1000.0, np.nan)
        df = tw.compute_liquidity_universe(values, top_n=1, window=20, freq="Q")
        # 3/31 時 NEW 只有 8 天資料，不夠 20 日不能入選
        self.assertEqual(df.loc[df["symbol"] == "A", "start"].tolist(), ["2020-04-01"])
        self.assertNotIn("NEW", df["symbol"].tolist())


@unittest.skipUnless(HAS_QLIB, "pyqlib is not installed")
class PipelineTest(unittest.TestCase):
    STOCKS = {
        "2330": "twse",
        "2317": "twse",
        "2454": "twse",
        "2881": "twse",
        "6488": "tpex",
        "5274": "tpex",
    }

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.base_dir = self.tmp.joinpath("tw")
        self.qlib_dir = self.tmp.joinpath("qlib")
        self.dates = pd.bdate_range("2022-01-03", "2023-12-29")
        self.raw = {"^TWII": make_raw(self.dates, 17000.0, seed=0)}
        self.raw["0050.TW"] = make_raw(self.dates, 140.0, seed=1)
        for i, (code, market) in enumerate(self.STOCKS.items()):
            ticker = code + tw.MARKET_SUFFIX[market]
            self.raw[ticker] = make_raw(
                self.dates,
                50.0 * (i + 1),
                seed=10 + i,
                ex_div="2023-07-03",
                dividend=2.0,
            )

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _fake_stock_list(self, token=None):
        info = pd.DataFrame(
            {
                "industry_category": ["x"] * len(self.STOCKS),
                "stock_id": list(self.STOCKS),
                "stock_name": list(self.STOCKS),
                "type": list(self.STOCKS.values()),
            }
        )
        return tw.filter_stock_info(info)

    def _fake_fetch(self, ticker, start, end):
        df = self.raw[ticker]
        return df[(df["date"] >= start) & (df["date"] < end)].copy()

    def test_run_builds_qlib_data(self):
        import qlib
        from qlib.config import C
        from qlib.data import D

        with mock.patch.object(
            tw, "fetch_finmind_stock_list", self._fake_stock_list
        ), mock.patch.object(tw, "fetch_yahoo", self._fake_fetch):
            tw.run(
                base_dir=str(self.base_dir),
                qlib_dir=str(self.qlib_dir),
                start="2022-01-01",
                end="2023-12-31",
                delay=0,
                top_n=3,
                window=20,
            )

        inst_dir = self.qlib_dir.joinpath("instruments")
        all_symbols = tw._read_instruments(inst_dir.joinpath("all.txt"))["symbol"]
        self.assertEqual(sorted(all_symbols), sorted("TW" + c for c in self.STOCKS))
        tpex = tw._read_instruments(inst_dir.joinpath("tpex.txt"))["symbol"]
        self.assertEqual(sorted(tpex), ["TW5274", "TW6488"])

        qlib.init(provider_uri=str(self.qlib_dir), region="tw")
        self.assertEqual(C.trade_unit, 1000)
        members = D.list_instruments(D.instruments("top3"), as_list=True)
        self.assertTrue(0 < len(members) <= len(self.STOCKS))

        fields = ["$close", "$factor", "$change", "$vwap"]
        feat = D.features(["TW2330", "TW0050"], fields, "2022-01-01", "2023-12-31")
        tsmc = feat.loc["TW2330"]
        raw = self.raw["2330.TW"].set_index("date")
        np.testing.assert_allclose(
            (tsmc["$close"] / tsmc["$factor"]).values, raw["close"].values, rtol=1e-5
        )
        self.assertFalse(feat.loc["TW0050", "$close"].isna().any())


if __name__ == "__main__":
    unittest.main()

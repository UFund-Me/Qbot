import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd

from pytrader.data import data_utils


class TestDataUtils(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        data_dir = Path(self.temp_dir.name) / "pytrader" / "data"
        self.indexes_dir = data_dir / "indexes"
        self.indexes_dir.mkdir(parents=True)
        self.module_path = data_dir / "data_utils.py"

    def write_prices(self, code, dates, closes=None):
        row_count = len(dates)
        if closes is None:
            closes = list(range(10, 10 + row_count))
        prices = pd.DataFrame(
            {
                "trade_date": dates,
                "ts_code": [code] * row_count,
                "open": closes,
                "high": [close + 1 for close in closes],
                "low": [close - 1 for close in closes],
                "close": closes,
                "vol": range(100, 100 + row_count),
            }
        )
        prices.to_csv(self.indexes_dir / f"{code}.csv")

    def test_load_from_file_renames_columns_and_uses_date_index(self):
        self.write_prices("AAA", [20200103, 20200102])

        with patch.object(data_utils, "__file__", str(self.module_path)):
            result = data_utils.load_from_file("AAA")

        self.assertEqual(
            list(result.columns),
            ["code", "open", "high", "low", "close", "date", "volume", "rate"],
        )
        self.assertEqual(result["code"].tolist(), ["AAA", "AAA"])
        self.assertEqual(result.index.name, "date")
        self.assertEqual(result.index.tolist(), ["20200102", "20200103"])

    def test_load_data_filters_multiple_codes_by_date(self):
        self.write_prices(
            "AAA",
            [20200103, 20191231, 20200104, 20200102],
            closes=[30, 10, 60, 20],
        )
        self.write_prices(
            "BBB",
            [20200104, 20200102, 20191231, 20200103],
            closes=[60, 80, 100, 40],
        )

        with patch.object(data_utils, "__file__", str(self.module_path)):
            result = data_utils.load_data(
                ["AAA", "BBB"], start_time="20200102", end_time="20200103"
            )

        self.assertEqual(
            result.index.tolist(),
            ["20200102", "20200102", "20200103", "20200103"],
        )
        self.assertEqual(set(result["code"]), {"AAA", "BBB"})
        self.assertTrue((result["date"] == result.index).all())

        expected_rates = {
            "AAA": {"20200102": 1.0, "20200103": 0.5},
            "BBB": {"20200102": -0.2, "20200103": -0.5},
        }
        for code, rates_by_date in expected_rates.items():
            code_rows = result[result["code"] == code]
            self.assertEqual(code_rows.index.tolist(), list(rates_by_date))
            for date, expected_rate in rates_by_date.items():
                self.assertAlmostEqual(code_rows.loc[date, "rate"], expected_rate)

    def test_default_benchmarks_are_not_shared_between_instances(self):
        first = data_utils.DataUtil(None)
        first.benchmarks.append("TEST")

        second = data_utils.DataUtil(None)

        self.assertEqual(first.benchmarks, ["000300.SH", "TEST"])
        self.assertEqual(second.benchmarks, ["000300.SH"])
        self.assertIsNot(first.benchmarks, second.benchmarks)

    def test_to_backtrader_dataframe_has_expected_columns(self):
        source = pd.DataFrame(
            {
                "code": ["AAA"],
                "open": [10.0],
                "high": [11.0],
                "low": [9.0],
                "close": [10.5],
                "volume": [100],
            },
            index=["20200102"],
        )

        result = data_utils.DataUtil(source).to_backtrader_dataframe(source)

        self.assertIsInstance(result.index, pd.DatetimeIndex)
        self.assertEqual(
            list(result.columns),
            ["open", "high", "low", "close", "volume", "openinterest"],
        )
        self.assertEqual(result["openinterest"].tolist(), [0])


if __name__ == "__main__":
    unittest.main()

"""台股日線資料下載，並轉成 qlib 格式。

流程（可用 `run` 一次跑完）：
    download   從 Yahoo Finance 下載上市、上櫃股票及基準指數的日線
    normalize  對齊交易日曆、還原權值（qlib 的 factor 慣例）、計算 change / vwap
    dump       用 dump_bin.py 轉成 qlib 二進位格式，並產生 twse / tpex 股票池
    universe   依過去成交值每季重選前 N 檔，產生動態股票池（例如 top200）

範例：
    python qbot/data/tw_collector.py run
    python qbot/data/tw_collector.py run --symbols_file my_list.txt --top_n 50
    python qbot/data/tw_collector.py download --start 2005-01-01 --skip_exists True

股票代碼在 qlib 中一律寫成 TW + 代號（TW2330、TW6488），
加權指數為 TWII，元大台灣50 為 TW0050。
詳細說明見 docs/03-智能策略/台股qlib工作流.md
"""

import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from loguru import logger

DEFAULT_BASE_DIR = "~/.qlib/stock_data/tw"
DEFAULT_QLIB_DIR = "~/.qlib/qlib_data/tw_data"
SOURCE_DIR_NAME = "source"
NORMALIZE_DIR_NAME = "normalize"
STOCK_LIST_FILE = "stock_list.csv"
FAILED_FILE = "failed.txt"

# qlib 代碼 -> Yahoo 代碼
BENCHMARKS = {"TWII": "^TWII", "TW0050": "0050.TW"}
CALENDAR_SYMBOL = "TWII"
# 指數沒有可靠的成交量，不套用「量為 0 視為停牌」的規則
INDEX_SYMBOLS = {"TWII"}

MARKET_SUFFIX = {"twse": ".TW", "tpex": ".TWO"}
SUFFIX_MARKET = {v: k for k, v in MARKET_SUFFIX.items()}
YAHOO_COLUMNS = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adjclose",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "stock_splits",
}
PRICE_FIELDS = ["open", "high", "low", "close"]
QLIB_FIELDS = PRICE_FIELDS + ["volume", "vwap", "factor", "change"]

FINMIND_URL = "https://api.finmindtrade.com/api/v4/data"
STOCK_CODE_PATTERN = re.compile(r"[1-9]\d{3}")


def _to_qlib_symbol(code: str) -> str:
    return f"TW{code}"


def _make_stock_list(
    codes: List[str],
    markets: List[str],
    names: Optional[List[str]] = None,
    industries: Optional[List[str]] = None,
) -> pd.DataFrame:
    n = len(codes)
    df = pd.DataFrame(
        {
            "code": codes,
            "market": markets,
            "name": names if names is not None else [""] * n,
            "industry": industries if industries is not None else [""] * n,
        }
    )
    df["symbol"] = df["code"].map(_to_qlib_symbol)
    df["yahoo"] = df["code"] + df["market"].map(MARKET_SUFFIX)
    return df[["symbol", "code", "market", "yahoo", "name", "industry"]]


def filter_stock_info(info: pd.DataFrame) -> pd.DataFrame:
    """從 FinMind TaiwanStockInfo 留下上市、上櫃的普通股（4 碼、非 0 開頭）。

    0 開頭的是 ETF，興櫃（type=emerging）流動性太低也排除。
    """
    df = info.copy()
    df["stock_id"] = df["stock_id"].astype(str).str.strip()
    df = df[df["type"].isin(list(MARKET_SUFFIX))]
    df = df[df["stock_id"].str.fullmatch(STOCK_CODE_PATTERN.pattern)]
    df = df.drop_duplicates("stock_id").sort_values("stock_id")
    return _make_stock_list(
        df["stock_id"].tolist(),
        df["type"].tolist(),
        df["stock_name"].tolist(),
        df["industry_category"].tolist(),
    )


def fetch_finmind_stock_list(token: Optional[str] = None, timeout: int = 30):
    """抓 FinMind 的台股清單（TaiwanStockInfo）。token 可省略，但請求額度較低。"""
    import requests

    token = token or os.environ.get("FINMIND_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(
        FINMIND_URL,
        params={"dataset": "TaiwanStockInfo"},
        headers=headers,
        timeout=timeout,
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") != 200 or not payload.get("data"):
        raise RuntimeError(f"FinMind TaiwanStockInfo failed: {payload.get('msg')}")
    return filter_stock_info(pd.DataFrame(payload["data"]))


def load_symbols_file(path) -> pd.DataFrame:
    """讀取自訂股票清單，每行一檔，# 之後為註解。

    可寫 2330（預設上市）、2330.TW、6488.TWO，代號後面可接名稱。
    """
    codes, markets, names = [], [], []
    for line in Path(path).expanduser().read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        token = parts[0].upper()
        code, dot, suffix = token.partition(".")
        market = SUFFIX_MARKET.get(f".{suffix}") if dot else "twse"
        if market is None or not STOCK_CODE_PATTERN.fullmatch(code):
            raise ValueError(f"Unrecognized symbol in {path}: {parts[0]}")
        codes.append(code)
        markets.append(market)
        names.append(parts[1] if len(parts) > 1 else "")
    df = _make_stock_list(codes, markets, names)
    return df.drop_duplicates("symbol").reset_index(drop=True)


def fetch_yahoo(ticker: str, start: str, end: str) -> pd.DataFrame:
    """下載 Yahoo 日線（不還原），回傳 date + 小寫欄位；查無資料時回傳空表。"""
    import yfinance as yf

    df = yf.Ticker(ticker).history(
        start=start, end=end, interval="1d", auto_adjust=False, actions=True
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.rename(columns=YAHOO_COLUMNS)
    df.index = pd.to_datetime(df.index)
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    df.index = df.index.normalize()
    df.index.name = "date"
    columns = [c for c in YAHOO_COLUMNS.values() if c in df.columns]
    return df[columns].reset_index()


def download(
    base_dir: str = DEFAULT_BASE_DIR,
    start: str = "2005-01-01",
    end: Optional[str] = None,
    symbols_file: Optional[str] = None,
    finmind_token: Optional[str] = None,
    max_workers: int = 4,
    delay: float = 0.5,
    retries: int = 3,
    retry_wait: float = 5.0,
    skip_exists: bool = False,
):
    """下載股票清單與日線到 base_dir/source。

    end 含當天，預設為今天。沒給 symbols_file 時從 FinMind 抓全部上市、上櫃股票。
    Yahoo 有流量限制，中斷後可加 --skip_exists True 只補抓缺的檔案。
    """
    base_dir = Path(base_dir).expanduser()
    source_dir = base_dir.joinpath(SOURCE_DIR_NAME)
    source_dir.mkdir(parents=True, exist_ok=True)

    if symbols_file:
        stocks = load_symbols_file(symbols_file)
    else:
        stocks = fetch_finmind_stock_list(finmind_token)
    stocks.to_csv(base_dir.joinpath(STOCK_LIST_FILE), index=False)
    logger.info(f"{len(stocks)} stocks in {base_dir.joinpath(STOCK_LIST_FILE)}")

    # yfinance 的 end 不含當天
    end = pd.Timestamp(end) if end else pd.Timestamp.today().normalize()
    end = (end + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    jobs = dict(BENCHMARKS)
    jobs.update(stocks.set_index("symbol")["yahoo"].to_dict())

    def _job(symbol: str, ticker: str) -> str:
        path = source_dir.joinpath(f"{symbol}.csv")
        if skip_exists and path.exists():
            return "skip"
        for attempt in range(retries):
            try:
                df = fetch_yahoo(ticker, start, end)
                break
            except Exception as e:  # yfinance 會丟各種網路、限流例外
                logger.warning(f"{ticker} attempt {attempt + 1} failed: {e}")
                if attempt + 1 < retries:
                    time.sleep(retry_wait * 2**attempt)
        else:
            return "error"
        time.sleep(delay)
        if df.empty:
            return "empty"
        df.to_csv(path, index=False)
        return "ok"

    results: Dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_job, s, t): s for s, t in jobs.items()}
        for i, future in enumerate(as_completed(futures), 1):
            results[futures[future]] = future.result()
            if i % 100 == 0 or i == len(futures):
                logger.info(f"download {i}/{len(futures)}")

    failed = sorted(s for s, r in results.items() if r in ("error", "empty"))
    base_dir.joinpath(FAILED_FILE).write_text("\n".join(failed), encoding="utf-8")
    counts = pd.Series(results).value_counts().to_dict()
    logger.info(f"download finished: {counts}")
    if failed:
        logger.warning(
            f"{len(failed)} symbols failed, see {base_dir.joinpath(FAILED_FILE)}; "
            "rerun with --skip_exists True to retry only the missing ones"
        )
    if CALENDAR_SYMBOL not in results or results[CALENDAR_SYMBOL] in ("error", "empty"):
        logger.warning("TWII download failed; normalize will fall back to stock dates")


def _source_files(base_dir: Path) -> Dict[str, Path]:
    source_dir = base_dir.joinpath(SOURCE_DIR_NAME)
    return {p.stem: p for p in sorted(source_dir.glob("*.csv"))}


def _read_source(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_calendar(base_dir) -> pd.DatetimeIndex:
    """以加權指數的交易日為日曆；沒有指數資料時改用所有股票有成交的日期。"""
    files = _source_files(Path(base_dir).expanduser())
    if CALENDAR_SYMBOL in files:
        df = _read_source(files[CALENDAR_SYMBOL])
        dates = df.loc[df["close"].notna(), "date"]
    else:
        logger.warning("TWII.csv not found, building calendar from stock dates")
        dates = []
        for symbol, path in files.items():
            if symbol in BENCHMARKS:
                continue
            df = _read_source(path)
            dates.extend(df.loc[df["volume"] > 0, "date"])
    return pd.DatetimeIndex(sorted(set(pd.to_datetime(dates))), name="date")


def normalize_symbol(
    df: pd.DataFrame,
    symbol: str,
    calendar: Optional[pd.DatetimeIndex] = None,
    is_index: bool = False,
) -> pd.DataFrame:
    """把 Yahoo 原始日線轉成 qlib 慣例（同 qlib yahoo collector 的 1d normalize）。

    - 價格為還原權值後再除以首日收盤價，volume 反向調整
    - factor = 還原價 / 原始價，qlib 用 close / factor 換回實際股價來計算整張交易
    - change 為還原收盤價的日報酬，用來判斷漲跌停（除息日不會被當成大跌）
    - vwap 用 (high + low + close) / 3 近似（Yahoo 沒有成交金額）
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates("date").set_index("date").sort_index()
    if calendar is not None and len(calendar) > 0:
        in_range = (calendar >= df.index.min()) & (calendar <= df.index.max())
        df = df.reindex(calendar[in_range])
        df.index.name = "date"
    if df.empty:
        return pd.DataFrame()
    if "adjclose" not in df.columns:
        df["adjclose"] = df["close"]

    invalid = df["close"].isna() | (df["close"] <= 0)
    if not is_index:
        invalid |= df["volume"].isna() | (df["volume"] <= 0)
    df.loc[invalid, PRICE_FIELDS + ["adjclose", "volume"]] = np.nan
    if df["close"].isna().all():
        return pd.DataFrame()

    df["factor"] = (df["adjclose"] / df["close"]).ffill()
    for col in PRICE_FIELDS:
        df[col] = df[col] * df["factor"]
    df["volume"] = df["volume"] / df["factor"]

    close = df["close"].ffill()
    df["change"] = close / close.shift(1) - 1
    df.loc[invalid, "change"] = np.nan

    first_close = df["close"].dropna().iloc[0]
    for col in PRICE_FIELDS + ["factor"]:
        df[col] = df[col] / first_close
    df["volume"] = df["volume"] * first_close
    df["vwap"] = (df["high"] + df["low"] + df["close"]) / 3

    df["symbol"] = symbol
    return df.reset_index()[["date", "symbol"] + QLIB_FIELDS]


def normalize(base_dir: str = DEFAULT_BASE_DIR):
    """把 base_dir/source 的原始資料轉到 base_dir/normalize。"""
    base_dir = Path(base_dir).expanduser()
    normalize_dir = base_dir.joinpath(NORMALIZE_DIR_NAME)
    normalize_dir.mkdir(parents=True, exist_ok=True)
    for old in normalize_dir.glob("*.csv"):
        old.unlink()

    calendar = load_calendar(base_dir)
    logger.info(f"calendar: {len(calendar)} days")
    count = 0
    for symbol, path in _source_files(base_dir).items():
        df = normalize_symbol(
            _read_source(path), symbol, calendar, is_index=symbol in INDEX_SYMBOLS
        )
        if df.empty:
            logger.warning(f"{symbol} has no valid rows, skipped")
            continue
        df.to_csv(normalize_dir.joinpath(f"{symbol}.csv"), index=False)
        count += 1
    logger.info(f"normalized {count} symbols into {normalize_dir}")


def _instruments_dir(qlib_dir) -> Path:
    path = Path(qlib_dir).expanduser().joinpath("instruments")
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_instruments(path: Path) -> pd.DataFrame:
    return pd.read_csv(
        path, sep="\t", header=None, names=["symbol", "start", "end"], dtype=str
    )


def _write_instruments(df: pd.DataFrame, path: Path):
    df[["symbol", "start", "end"]].to_csv(path, sep="\t", header=False, index=False)


def write_market_instruments(
    base_dir: str = DEFAULT_BASE_DIR, qlib_dir: str = DEFAULT_QLIB_DIR
):
    """從 all.txt 移除基準指數，並依股票清單拆出 twse.txt、tpex.txt。"""
    inst_dir = _instruments_dir(qlib_dir)
    all_path = inst_dir.joinpath("all.txt")
    inst = _read_instruments(all_path)
    inst = inst[~inst["symbol"].isin(list(BENCHMARKS))]
    _write_instruments(inst, all_path)

    stock_list_path = Path(base_dir).expanduser().joinpath(STOCK_LIST_FILE)
    if not stock_list_path.exists():
        return
    stocks = pd.read_csv(stock_list_path, dtype=str)
    for market in MARKET_SUFFIX:
        symbols = set(stocks.loc[stocks["market"] == market, "symbol"])
        _write_instruments(
            inst[inst["symbol"].isin(symbols)], inst_dir.joinpath(f"{market}.txt")
        )


def dump(
    base_dir: str = DEFAULT_BASE_DIR,
    qlib_dir: str = DEFAULT_QLIB_DIR,
    max_workers: int = 8,
):
    """用 dump_bin.py 把 base_dir/normalize 轉成 qlib 格式（會覆寫 qlib_dir 的日曆）。"""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from dump_bin import DumpDataAll

    normalize_dir = Path(base_dir).expanduser().joinpath(NORMALIZE_DIR_NAME)
    DumpDataAll(
        csv_path=str(normalize_dir),
        qlib_dir=qlib_dir,
        max_workers=max_workers,
        date_field_name="date",
        symbol_field_name="symbol",
        include_fields=",".join(QLIB_FIELDS),
    )()
    write_market_instruments(base_dir, qlib_dir)


def compute_liquidity_universe(
    values: pd.DataFrame, top_n: int = 200, window: int = 60, freq: str = "Q"
) -> pd.DataFrame:
    """依過去 window 日平均成交值，在每期最後一個交易日收盤後選出前 top_n 檔。

    values：index 為交易日，columns 為代碼，上市前或下市後為 NaN，停牌日為 0。
    選股只用當天（含）以前的資料，成分從下一個交易日生效，到下一次重選日為止，
    所以沒有前視偏差。回傳 symbol / start / end，連續入選的期間會合併成一段。
    """
    dates = values.index
    avg = values.rolling(window, min_periods=window).mean()
    periods = dates.to_period(freq)
    rebalance_dates = dates[~periods.duplicated(keep="last")]

    spans: Dict[str, List[list]] = {}
    for i, rebalance in enumerate(rebalance_dates):
        pos = dates.get_loc(rebalance)
        if pos + 1 >= len(dates):
            break
        ranked = avg.loc[rebalance].dropna()
        ranked = ranked[ranked > 0].nlargest(top_n)
        start = dates[pos + 1]
        if i + 1 < len(rebalance_dates):
            end = rebalance_dates[i + 1]
        else:
            end = dates[-1]
        for symbol in ranked.index:
            symbol_spans = spans.setdefault(symbol, [])
            # 上一期也有入選（上一段剛好結束在這次重選日）就延長
            if symbol_spans and symbol_spans[-1][1] == rebalance:
                symbol_spans[-1][1] = end
            else:
                symbol_spans.append([start, end])

    rows = [
        (symbol, start, end)
        for symbol, symbol_spans in sorted(spans.items())
        for start, end in symbol_spans
    ]
    df = pd.DataFrame(rows, columns=["symbol", "start", "end"])
    for col in ("start", "end"):
        df[col] = pd.to_datetime(df[col]).dt.strftime("%Y-%m-%d")
    return df


def _load_trading_values(base_dir: Path, calendar: pd.DatetimeIndex) -> pd.DataFrame:
    stock_list_path = base_dir.joinpath(STOCK_LIST_FILE)
    stocks = set(pd.read_csv(stock_list_path, dtype=str)["symbol"])
    values = {}
    for symbol, path in _source_files(base_dir).items():
        if symbol not in stocks:
            continue
        df = _read_source(path).drop_duplicates("date").set_index("date").sort_index()
        # Yahoo 的 close 只做分割調整、未除息，乘上成交量即為當日成交值
        value = (df["close"] * df["volume"]).clip(lower=0)
        in_range = (calendar >= df.index.min()) & (calendar <= df.index.max())
        values[symbol] = value.reindex(calendar[in_range]).fillna(0)
    return pd.DataFrame(values).reindex(calendar)


def universe(
    base_dir: str = DEFAULT_BASE_DIR,
    qlib_dir: str = DEFAULT_QLIB_DIR,
    top_n: int = 200,
    window: int = 60,
    freq: str = "Q",
    name: Optional[str] = None,
):
    """產生動態股票池 instruments/<name>.txt（預設 top200，每季重選）。"""
    base_dir = Path(base_dir).expanduser()
    name = name or f"top{top_n}"
    calendar = load_calendar(base_dir)
    values = _load_trading_values(base_dir, calendar)
    df = compute_liquidity_universe(values, top_n=top_n, window=window, freq=freq)
    path = _instruments_dir(qlib_dir).joinpath(f"{name}.txt")
    _write_instruments(df, path)
    logger.info(f"universe {name}: {df['symbol'].nunique()} symbols -> {path}")


def run(
    base_dir: str = DEFAULT_BASE_DIR,
    qlib_dir: str = DEFAULT_QLIB_DIR,
    start: str = "2005-01-01",
    end: Optional[str] = None,
    symbols_file: Optional[str] = None,
    finmind_token: Optional[str] = None,
    max_workers: int = 4,
    delay: float = 0.5,
    skip_exists: bool = False,
    top_n: int = 200,
    window: int = 60,
    freq: str = "Q",
):
    """依序執行 download、normalize、dump、universe。"""
    download(
        base_dir,
        start=start,
        end=end,
        symbols_file=symbols_file,
        finmind_token=finmind_token,
        max_workers=max_workers,
        delay=delay,
        skip_exists=skip_exists,
    )
    normalize(base_dir)
    dump(base_dir, qlib_dir)
    universe(base_dir, qlib_dir, top_n=top_n, window=window, freq=freq)


if __name__ == "__main__":
    import fire

    fire.Fire(
        {
            "run": run,
            "download": download,
            "normalize": normalize,
            "dump": dump,
            "universe": universe,
        }
    )

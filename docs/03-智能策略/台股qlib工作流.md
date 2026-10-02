## 台股 qlib 工作流

用 Yahoo Finance 的台股日線建立 qlib 資料，再用 Alpha158 因子 + LightGBM 選股並回測。

- 資料腳本：[qbot/data/tw_collector.py](../../qbot/data/tw_collector.py)
- 回測設定：[workflow_config_lightgbm_Alpha158_tw.yaml](../../pytrader/strategies/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158_tw.yaml)

### 安裝

```bash
pip install "pyqlib>=0.8.6" lightgbm yfinance fire loguru requests
```

`region: tw` 需要 pyqlib 0.8.6 以上。

### 1. 建立資料

```bash
python qbot/data/tw_collector.py run
```

會依序執行下面四步，也可以分開跑：

| 步驟 | 做什麼 | 輸出 |
|---|---|---|
| `download` | 從 FinMind 取得上市、上櫃普通股清單，從 Yahoo 下載 2005 年起的日線、加權指數與 0050 | `~/.qlib/stock_data/tw/source/` |
| `normalize` | 以加權指數的交易日為日曆對齊、還原權值、計算 `change` 與 `vwap` | `~/.qlib/stock_data/tw/normalize/` |
| `dump` | 轉成 qlib 二進位格式，並產生 `all`、`twse`、`tpex` 股票池 | `~/.qlib/qlib_data/tw_data/` |
| `universe` | 依過去 60 日平均成交值每季重選前 200 檔，產生 `top200` 股票池 | `instruments/top200.txt` |

常用參數：

```bash
# FinMind token（可省略，有 token 的請求額度較高），也可設環境變數 FINMIND_TOKEN
python qbot/data/tw_collector.py run --finmind_token <token>

# Yahoo 有流量限制，下載中斷後只補抓缺的檔案
python qbot/data/tw_collector.py download --skip_exists True

# 自訂股票清單：每行一檔，2330（預設上市）、2330.TW、6488.TWO，# 之後為註解
python qbot/data/tw_collector.py run --symbols_file my_list.txt --top_n 50

# 改股票池：前 100 檔、每月重選
python qbot/data/tw_collector.py universe --top_n 100 --freq M
```

更新資料時重新執行 `run` 即可（會重建整個資料夾）。下載失敗的代碼記錄在 `~/.qlib/stock_data/tw/failed.txt`。

qlib 中的代碼一律寫成 `TW` + 代號，例如 `TW2330`、`TW6488`；加權指數為 `TWII`，元大台灣50 為 `TW0050`。

### 2. 訓練與回測

```bash
qrun pytrader/strategies/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158_tw.yaml
```

結果存在執行目錄下的 `mlruns/`，會印出 IC / Rank IC 與扣除成本前後的超額報酬。畫圖可參考 [pytrader/analyser/workflow.py](../../pytrader/analyser/workflow.py)。

### 設定說明

| 設定 | 值 | 原因 |
|---|---|---|
| `region` | `tw` | 交易單位 1000 股（一張）。買進一律整張；qlib 以還原價把股息視為再投入，持有部位經過除息後換算股數會略偏離整張，全部賣出時也就不是整張 |
| `market` | `top200` | 動態股票池，只用重選日（含）以前的成交值，從下一個交易日生效，沒有前視偏差；避免用「現在的台灣50成分股」回測過去 |
| `benchmark` | `TW0050` | 0050 的還原價含息；`TWII` 是不含息的價格指數，拿來當基準會讓超額報酬每年虛增約一個殖利率 |
| `limit_threshold` | `0.095` | 漲停價依升降單位向下取整，實際漲停幅度約 9.5%～10%，用 0.1 會漏掉大部分漲停 |
| `open_cost` / `close_cost` | `0.001425` / `0.004425` | 手續費 0.1425%，賣出另加證交稅 0.3%；有券商折扣可自行調低 |
| `min_cost` | `20` | 最低手續費 20 元 |
| `account` | `1000000000` | 高價股一張動輒數百萬，帳戶太小會買不到；小資金可在 `exchange_kwargs` 加 `trade_unit: 1` 模擬零股（2020-10-26 起開放盤中零股） |
| 回測期間 | 2021～2025 | 2015-06-01 前漲跌幅是 7%，`limit_threshold` 不適用 |

### 改用其他模型

repo 內其他 benchmark（XGBoost、MLP、Transformer…）的 yaml 都是 A 股設定，照下面改即可套用台股：

1. `qlib_init`：`provider_uri: "~/.qlib/qlib_data/tw_data"`、`region: tw`
2. `market: top200`、`benchmark: TW0050`
3. `exchange_kwargs`：`limit_threshold`、`open_cost`、`close_cost`、`min_cost` 改成上表的值
4. 資料、訓練、回測的日期改成台股資料的範圍
5. 策略參數用 `signal: <PRED>`（repo 內舊 yaml 寫的 `model: <MODEL>` / `dataset: <DATASET>` 是舊版 qlib 的寫法）

### 限制

- **倖存者偏差**：股票清單只有目前上市、上櫃的公司，Yahoo 也查不到已下市股票，回測績效會偏高
- **VWAP 是近似值**：Yahoo 沒有成交金額，`vwap` 用 (最高 + 最低 + 收盤) / 3
- **Yahoo 資料品質**：偶有錯價或缺漏，重要結論請用其他資料源交叉驗證
- **漲跌停判斷是近似**：以 9.5% 判斷，少數漲幅 9.5%～10% 但沒漲停的日子會被當成漲停
- **沒有基本面資料**：本工作流只有量價因子；財報、月營收、三大法人等需另外串接（例如 FinMind）

### 常見問題

- **回測出現 `IndexError: index ... is out of bounds`**：資料最後一天必須晚於回測 `end_time`，qlib 回測需要下一個交易日
- **`MlflowException: The filesystem tracking backend ... is in maintenance mode`**：新版 MLflow 預設不讓 qlib 用 `mlruns/` 資料夾，執行前設定 `export MLFLOW_ALLOW_FILE_STORE=true`

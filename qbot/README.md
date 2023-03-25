
Qbot core engine


```
.
├── RREADME.md
├── config
│   └── national_holidays.csv
├── easyuncle
│   └── README.md
├── main.py
├── strategies
│   ├── README.md
│   ├── bigger_than_ema_bt.py
│   └── bt_boll.py
└── vnpy
    └── README.md
```

说明：
- 主程序：main.py
- 交易策略：strategies，更多股票和基金交易策略在pyfund和``pytader/*_strategies``实现。
- 配置项：configs
- 自动化交易引擎 vnpy + ci
- 多账本管理 easyuncle
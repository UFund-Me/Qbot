# 分层设计、事件驱动

## 分层设计

[数据层](qbot/data/)：数据获取抽象封装

[策略层](qbot/strategy/)：多因子、动量、机器学习、强化学习、深度学习策略

[Engine层](qbot/engine/)：回测引擎、模拟交易、实盘交易

[接口层](qbot/engine/trading/)：交易接口封装，包含多平台的模拟和实盘交易

[通知层](qbot/notify/)：系统监控服务、消息通知（系统弹窗、邮件、飞书、微信、钉钉、企业微信等）                         

[分析层](qbot/analyser/)：原始数据清洗、股票[指标](qbot/engine/indicator/)、[算子库](qbot/engine/algo/)、评测结果分析

[扩展层](qbot/extension/)：其他功能插件服务，如[QInvestool](backend/investool/)、[fund-strategies 基金分析工具](backend/fund-strategies/)、[股票基金管家](frontend/web-extension)等

> [!NOTE] (Charmve):
> 接口层和Engine层会考虑重新调整。

## 前后端分离

1. 前端主要是客户端显示和分析评测工具web网页

2. 后端插件服务：主要是股票、基金分析工具作为后台引入qbot客户端
- [fund-strategies 基金分析工具](backend/fund-strategies/) - 基金分析、基金评测、4433基金选择、策略评测
- [QInvestool](backend/investool/) - 基金、股票评测，选股，因子挖掘
- 浏览器插件：[股票基金管家](frontend/web-extension)

## 开发语言

整个Qbot开发语言主要是Python，基于wxPython gui框架搭建而成。另外，后台插件服务QInvestool采用go语言开发、fund-strategies 基金分析工具和股票基金管家浏览器插件采用JavaScript开发.

- WXPython 开发手册 https://wizardforcel.gitbooks.io/wxpy-in-action/content/6.html
- 
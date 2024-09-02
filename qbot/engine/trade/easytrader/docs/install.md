### requirements

### 客户端设置

需要对客户端按以下设置，不然会导致下单时价格出错以及客户端超时锁定

* 系统设置 > 界面设置: 界面不操作超时时间设为 0
* 系统设置 > 交易设置: 默认买入价格/买入数量/卖出价格/卖出数量 都设置为 空

同时客户端不能最小化也不能处于精简模式

### 云端部署建议

在云服务上部署时，使用自带的远程桌面会有问题，推荐使用 TightVNC

### 登陆时的验证码识别

券商如果登陆需要识别验证码的话需要安装 tesseract：

* `tesseract` : 非 `pytesseract`, 需要单独安装, [地址](https://github.com/tesseract-ocr/tesseract/wiki),保证在命令行下 `tesseract` 可用

或者你也可以手动登陆后在通过 `easytrader` 调用，此时 `easytrader` 在登陆过程中会直接识别到已登陆的窗口。

### 安装

```shell
pip install easytrader
```

注： `Windows` 用户 `pip` 安装时会提示 `No module named xxx`, 请使用 `pip install xxx` 安装对应缺失的 `module`, 然后再重新 `pip install easytrader`, 可以参考此文档 [INSTALL4Windows.md](other/INSTALL4Windows.md)

### 升级

```shell
pip install easytrader -U
```


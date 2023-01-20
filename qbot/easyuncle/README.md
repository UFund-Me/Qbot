# easyuncle
EasyUncle（账本叔叔）是一个基于easytrader(https://github.com/shidenggui/easytrader)封装的适用于多账户，多策略，有高可用性的下单/持仓管理模块

## easyuncle初始化

### 读取数据库配置(./db.json)
#### 连接数据库
#### 数据库配置文件格式
```
{
  "type"          : "mongodb",
  "port"          : 27017,
  "username"      : "username",
  "pwd"           : "password"
  "db_name"       : "easyuncle",
}
```

### 读取帐号配置(./accounts.json文件)
> accounts.json范例, 其中key是用于给自己识别的自定义的名字，建议用英文, 每个账户中用"brokerage"来标识券商，这里"yh"代表是银河，之后会调用easytrader.use("yh")
```
{
  "account_1"  : { "username": "username", "pwd" : "password", "brokerage": "yh" },
  "account_2"  : { "username": "username", "pwd" : "password", "brokerage": "yh" },
}
```
#### 开启多个easytrader实例，以登录多个账户，检查持仓，本地化。
#### 

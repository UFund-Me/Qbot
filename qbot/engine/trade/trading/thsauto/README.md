# thsauto
同花顺自动下单工具

```
python .\server.py  192.168.0.116 5000 C:\Users\match\Desktop\THS\xiadan.exe
```
- 查询资金账户  
http://192.168.0.116:5000/thsauto/balance  
- 查询持仓  
http://192.168.0.116:5000/thsauto/position  
- 买入下单  
http://192.168.0.116:5000/thsauto/buy?stock_no=600000&price=10.00&amount=100  
- 卖出下单  
http://192.168.0.116:5000/thsauto/sell?stock_no=600000&price=10.00&amount=100  
- 科创板买入下单  
http://192.168.0.116:5000/thsauto/buy/kc?stock_no=688819&price=40.00&amount=200  
- 科创板卖出下单  
http://192.168.0.116:5000/thsauto/sell/kc?stock_no=688819&price=40.00&amount=200  
- 查询未成订单  
http://192.168.0.116:5000/thsauto/orders/active  
- 查询已成订单  
http://192.168.0.116:5000/thsauto/orders/filled  
- 撤单  
http://192.168.0.116:5000/thsauto/cancel?entrust_no=2060704404  
- 关闭同花顺客户端  
http://192.168.0.116:5000/thsauto/client/kill  
- 重启同花顺客户端  
http://192.168.0.116:5000/thsauto/client/restart 



more: https://blog.csdn.net/liuyukuan/article/details/117828103 

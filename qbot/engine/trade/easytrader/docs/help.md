# 某些同花顺客户端不允许拷贝 `Grid` 数据

现在默认获取 `Grid` 数据的策略是通过剪切板拷贝，有些券商不允许这种方式，导致无法获取持仓等数据。为解决此问题，额外实现了一种通过将 `Grid` 数据存为文件再读取的策略，
使用方式如下:

```python
from easytrader import grid_strategies

user.grid_strategy = grid_strategies.Xls
```

# 通过工具栏刷新按钮刷新数据

当前的刷新数据方式是通过切换菜单栏实现，通用但是比较缓慢，可以选择通过点击工具栏的刷新按钮来刷新

```python
from easytrader import refresh_strategies

# refresh_btn_index 指的是刷新按钮在工具栏的排序，默认为第四个，根据客户端实际情况调整
user.refresh_strategy = refresh_strategies.Toolbar(refresh_btn_index=4)
```

# 无法保存对应的 xls 文件

有些系统默认的临时文件目录过长，使用 xls 策略时无法正常保存，可通过如下方式修改为自定义目录

```
user.grid_strategy_instance.tmp_folder = 'C:\\custom_folder'
```

# 某些券商客户端无法输入文本

有些客户端无法通过 set_edit_text 方法输入内容，可以通过使用 type_keys 方法绕过，开启方式

```
user.enable_type_keys_for_editor()
```

# 如何关闭 debug 日志的输出

```python
user = easytrader.use('yh', debug=False)

```


# 编辑配置文件，运行后出现 `json` 解码报错


出现如下错误

```python
raise JSONDecodeError("Expecting value", s, err.value) from None

JSONDecodeError: Expecting value
```

请勿使用 `记事本` 编辑账户的 `json` 配置文件，推荐使用 [notepad++](https://notepad-plus-plus.org/zh/) 或者 [sublime text](http://www.sublimetext.com/)

### 其他

[软件实现原理](http://www.jisilu.cn/question/42707)

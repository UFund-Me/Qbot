trader
======

操盘大哥的交易组件


INSTALL
=======

先装talib的C库，再用pip装依赖。

修改 mysql 配置文件 /etc/my.cnf.d/server.cnf ，增加如下配置:

    [mysqld]

    wait_timeout=31536000

    interactive_timeout=31536000

重启mysql服务

License
-------

``trader`` is offered under the Apache 2 license.

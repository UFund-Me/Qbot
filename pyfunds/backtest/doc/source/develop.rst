=============
开发者文档
=============

欢迎直接在 GitHub 提交 issue 或发起 PR。


工作流
----------

git部分：fork 仓库，clone 到本地修改，push 回 forked 仓库，提交 PR 到 master 分支。关于中间涉及的 git 操作，如在本地保持和原始库更新同步等，这里不再赘述。

测试部分：测试基于 pytest, ``cd tests && pytest`` 即可，请注意测试时 pwd 需为 tests 文件夹。单独测试可用 ``pytest test_file.py::test_func``。

linter 部分：使用 ``black`` 及其默认设置，提交代码前请运行 ``black .``。

文档部分：使用 ``sphnix`` 工作流，本地预览可以 ``cd doc && make html``, 生成的网页在 ``doc/build/html`` 中。

如果添加新功能请注意添加对应的测试案例到 tests 中，新函数请保证必要的 docstring，如有必要，请相应修改 CHANGELOG.md 的内容。
也可添加文档介绍新功能到 ``doc/source`` 中或新的案例分析 jupyter notebook 到 ``doc/sample`` 中。


欢迎的贡献方向
----------------

任何 PR 和讨论都是欢迎的，但以下方向可能在优先级上靠前。

0. 找到并修正现存的明显的 bug。

1. 代码，文档，repo 任何位置的中英文 typo。

2. 可以测试 corner case 或增加代码覆盖的更多新测试案例。

3. ``xa.cons.droplist`` 元素添加，也即找到更多份额舍掉零头而非四舍五入的基金。

4. 完善已有函数的 docstring，完善和增加文档及案例。

5. 增加有趣的基于 xalpha 的案例分析，作为独立的 jupyter notebook。

6. 保证对外接口不变情况下的，冗余代码小幅重构。

7. 依赖库跨版本更新造成的 broken API 的发现和修复。

8. 为 ``xa.universal.get_daily`` 增加更多的数据源爬虫后端。

9. 将更多聚宽的数据，合理的设计和封装到 ``xa.universal.get_daily``。

10. 为 ``xa.indicator.indicator`` 增加更多的技术指标计算。

11. pyecharts 可视化部分的效果优化和选项调整。


对于更激进的新功能大幅增加或代码重构，需鉴权数据提供方的添加，API调整等，建议先开 issue 进行讨论，防止重复或无效工作。


常见问题
-------------

* 运行 pytest 时，如果报错 ``AttributeError: ‘Function’ object has no attribute ‘get_marker’``，可以参考 `链接 <https://www.scivision.dev/pytest-attribute-error-getmarker/>`_，对pytest-cov做个升级.


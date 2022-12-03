import importlib

_modules = {}
custom_folder = 'custom_strategies'
imp_class = 'Strategy'


def new_module(module_name):
    return importlib.import_module('.' + module_name, custom_folder)


def load_strategy_class(code: str, name: str):
    """
    加载策略文件
    :param code:
    :param name:
    :return:
    """
    with open(custom_folder + "/" + name + ".py", 'w', encoding='utf8') as file:
        file.write(code)
        file.close()

    if name in _modules:
        strategy_module = _modules.get(name)
        strategy_module = importlib.reload(strategy_module)
    else:
        strategy_module = new_module(name)

    return getattr(strategy_module, imp_class)


if __name__ == '__main__':
    code = open('strategies/example.py', encoding='utf8').read()
    strategy_module_cls = load_strategy_class(code, 'test')
    print(strategy_module_cls)

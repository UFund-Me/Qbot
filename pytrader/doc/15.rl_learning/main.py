import os
import pickle
import pandas as pd
import random
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from rlenv.StockTradingEnv0 import StockTradingEnv
from tasks import multi_stock_trade
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font = fm.FontProperties(fname='font/wqy-microhei.ttc')
# plt.rc('font', family='Source Han Sans CN')
plt.rcParams['axes.unicode_minus'] = False
os.environ["CUDA_VISIBLE_DEVICES"] = "1"


def stock_trade(stock_file):
    day_profits = []
    df = pd.read_csv(stock_file)
    df = df.sort_values('date')

    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: StockTradingEnv(df)])

    model = PPO2(MlpPolicy, env, verbose=0, tensorboard_log='./log', gamma=0.95, n_steps=20, learning_rate=2.5e-2)
    model.learn(total_timesteps=int(1e5))

    df_test = pd.read_csv(stock_file.replace('train', 'test'))

    env = DummyVecEnv([lambda: StockTradingEnv(df_test)])
    obs = env.reset()
    for i in range(len(df_test) - 1):
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        profit = env.render()
        day_profits.append(profit)
        if done:
            break
    return day_profits


def find_file(path, name):
    # print(path, name)
    for root, dirs, files in os.walk(path):
        for fname in files:
            if name in fname:
                return os.path.join(root, fname)


def test_a_stock_trade(stock_code):
    stock_file = find_file('./stockdata/train', str(stock_code))

    daily_profits = stock_trade(stock_file)
    fig, ax = plt.subplots()
    ax.plot(daily_profits, '-o', label=stock_code, marker='o', ms=10, alpha=0.7, mfc='orange')
    ax.grid()
    plt.xlabel('step')
    plt.ylabel('profit')
    ax.legend(prop=font)
    # plt.show()
    plt.savefig(f'./img/{stock_code}.png')


def analysis_profits(results):
    is_profit = [p[-1] for p in results]
    len(is_profit)
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    font = fm.FontProperties(fname='./font/wqy-microhei.ttc')

    labels = 'Profit', 'Loss', '0'

    sizes = [0, 0, 0]

    for p in is_profit:
        if p > 0:
            sizes[0] += 1
        if p < 0:
            sizes[1] += 1
        else:
            sizes[2] += 1

    explode = (0.1, 0.05, 0.05)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.legend(prop=font)
    plt.show()
    plt.savefig('./img/profits.png')

    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    font = fm.FontProperties(fname='./font/wqy-microhei.ttc')
    n_bins = 150

    fig, axs = plt.subplots()
    axs.hist(is_profit, bins=n_bins, density=True)
    plt.savefig('./img/profits_hist.png')


if __name__ == '__main__':
    files = os.listdir("stockdata/train")
    files_test = os.listdir("stockdata/test")
    all_files_list = list(set(files) & set(files_test))
    for i in all_files_list:
        # 使用celery做并发
        code = ".".join(i.split(".")[:2])
        multi_stock_trade.apply_async(args=(code,))
        # multi_stock_trade(code)

    import pickle
    files = os.listdir("result")
    results = []
    for f_name in files:
        f = open(f"result/{f_name}", "rb")
        data = pickle.load(f)
        results.append(data[-1])
    analysis_profits(results)

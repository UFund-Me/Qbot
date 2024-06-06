import os
import pickle
import pandas as pd
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from rlenv.StockTradingEnv0 import StockTradingEnv
from celery import Celery

BROKER_URL = f'redis://127.0.0.1:6379/0'
BACKEND_URL = f'redis://127.0.0.1:6379/0'

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# 新建celery任务
app = Celery('rl', broker=BROKER_URL, backend=BACKEND_URL)


def stock_trade(stock_file):
    day_profits = []
    df = pd.read_csv(stock_file)
    df = df.sort_values('date')

    # The algorithms require a vectorized environment to run
    env = DummyVecEnv([lambda: StockTradingEnv(df)])

    model = PPO2(MlpPolicy, env, verbose=0, tensorboard_log='./log')
    model.learn(total_timesteps=int(1e4))

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


@app.task
def multi_stock_trade(code):
    stock_file = find_file('./stockdata/train', str(code))
    if stock_file:
        profits = stock_trade(stock_file)
        with open(f'result/code-{code}.pkl', 'wb') as f:
            pickle.dump(profits, f)

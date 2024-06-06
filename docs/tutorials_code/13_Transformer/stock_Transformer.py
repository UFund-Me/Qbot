# 导入必要的库
import copy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.family"] = ["SimHei"]  # 设置字体为 'Arial Unicode MS'
from sklearn.preprocessing import MinMaxScaler

# 加载数据
price_df = pd.read_parquet("stock_price_20230522.parquet")

seq_len = 24


# 构建数据集
def create_dataset(data, seq_len):
    X, Y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i : i + seq_len])
        Y.append(data[i + seq_len])
    return np.array(X), np.array(Y)


# 数据标准化
def normalization(data, label):
    mm_x = MinMaxScaler()
    mm_y = MinMaxScaler()
    label = label.reshape(-1, 1)
    data = mm_x.fit_transform(data)  # 对数据和标签进行标准化
    label = mm_y.fit_transform(label)
    return data, label, mm_y


# 训练集、测试集切分
def split_data(x, y, split_ratio):
    train_size = int(len(y) * split_ratio)
    x_data = np.array(x)
    y_data = np.array(y)
    x_train = np.array(x[0:train_size])
    y_train = np.array(y[0:train_size])
    y_test = np.array(y[train_size : len(y)])
    x_test = np.array(x[train_size : len(x)])
    return x_data, y_data, x_train, y_train, x_test, y_test


X = None
Y = None
col_list = list(price_df.columns)[1]
if not isinstance(col_list, list):
    col_list = [col_list]
for col in col_list:
    data = np.array(price_df[col])
    X0, Y0 = create_dataset(data, seq_len)
    if X is None:
        X = copy.deepcopy(X0)
        Y = copy.deepcopy(Y0)
    else:
        X = np.concatenate([X, X0])
        Y = np.concatenate([Y, Y0])

X, Y, mm_y = normalization(X, Y)
# 划分训练集和测试集
train_size = int(len(X) * 0.7)
X, Y, X_train, Y_train, X_test, Y_test = split_data(X, Y, 0.7)


# 定义模型
class TransformerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, num_heads, dropout_rate):
        super().__init__()
        self.encoder_layer = nn.TransformerEncoderLayer(
            input_dim, num_heads, hidden_dim, dropout_rate
        )
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers)
        self.fc = nn.Linear(input_dim, 1)

    def forward(self, x):
        x = self.transformer_encoder(x)
        x = self.fc(x)
        return x


# 训练模型
input_dim = seq_len
hidden_dim = 512
num_layers = 2
num_heads = 8
dropout_rate = 0.1
batch_size = 100
learning_rate = 0.001
num_epochs = 100

model = TransformerModel(input_dim, hidden_dim, num_layers, num_heads, dropout_rate)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
for epoch in range(num_epochs):
    trainset_output_y = np.array([]).reshape(-1, 1)
    for i in range(0, len(X_train), batch_size):
        optimizer.zero_grad()
        batch_X = torch.tensor(X_train[i : i + batch_size]).float()
        batch_Y = torch.tensor(Y_train[i : i + batch_size]).float()
        output = model(batch_X)
        loss = criterion(output, batch_Y)
        loss.backward()
        optimizer.step()
        trainset_output_y = np.concatenate([trainset_output_y, output.detach().numpy()])

    if epoch % 10 == 0:
        print("Epoch: %d, Loss: %.5f" % (epoch, loss.item()))


# 预测结果
model.eval()
Y_pred = np.array([]).reshape(-1, 1)
for i in range(0, len(X_test), batch_size):
    batch_X = torch.tensor(X_test[i : i + batch_size]).float()
    output = model(batch_X)
    Y_pred = np.concatenate([Y_pred, output.detach().numpy()])

# Y_pred = model(torch.tensor(X_test).float()).detach().numpy()
# 计算误差
mse = np.mean((Y_pred - Y_test) ** 2)
rmse = np.sqrt(mse)
mape = np.mean(np.abs((Y_pred - Y_test) / Y_test))
print("RMSE: %.5f, MAPE: %.5f%%" % (rmse, mape * 100))

Y_pred = mm_y.inverse_transform(Y_pred)
Y = mm_y.inverse_transform(Y.reshape(-1, 1))
trainset_output_y = mm_y.inverse_transform(trainset_output_y)
# 绘图
plt.figure()
plt.plot(Y, color="orange", linestyle="--")
# plt.plot(range(train_size), Y_pred[:train_size], color='green')
plt.plot(range(train_size), trainset_output_y, color="green")
plt.plot(range(train_size, len(Y)), Y_pred, color="blue")
plt.legend(("真实值", "预测值-训练集", "预测值-测试集"), fontsize="15")
plt.show()
plt.clf()

a = 1

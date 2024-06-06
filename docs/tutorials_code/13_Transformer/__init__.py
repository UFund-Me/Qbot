import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler

# 加载数据
data = pd.read_csv('stock_prices.csv', usecols=['close'])
data = data.dropna()
data = data.values.reshape(-1, 1)

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

# 构建数据集
def create_dataset(data, seq_len):
    X, Y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        Y.append(data[i+seq_len])
    return np.array(X), np.array(Y)

seq_len = 10
X, Y = create_dataset(data, seq_len)

# 划分训练集和测试集
train_size = int(len(X) * 0.7)
X_train, Y_train = X[:train_size], Y[:train_size]
X_test, Y_test = X[train_size:], Y[train_size:]

# 定义模型
class TransformerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, num_heads, dropout_rate):
        super().__init__()
        self.encoder_layer = nn.TransformerEncoderLayer(input_dim, num_heads, hidden_dim, dropout_rate)
        self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer, num_layers)
        self.fc = nn.Linear(input_dim, 1)

    def forward(self, x):
        x = self.transformer_encoder(x)
        x = self.fc(x[-1])
        return x

# 训练模型
input_dim = seq_len
hidden_dim = 256
num_layers = 2
num_heads = 8
dropout_rate = 0.2
batch_size = 32
learning_rate = 0.001
num_epochs = 100

model = TransformerModel(input_dim, hidden_dim, num_layers, num_heads, dropout_rate)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for i in range(0, len(X_train), batch_size):
        optimizer.zero_grad()
        batch_X = torch.tensor(X_train[i:i+batch_size]).float()
        batch_Y = torch.tensor(Y_train[i:i+batch_size]).float()
        output = model(batch_X)
        loss = criterion(output, batch_Y)
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        print('Epoch: %d, Loss: %.5f' % (epoch, loss.item()))

# 预测结果
model.eval()
X_test = torch.tensor(X_test).float()
Y_pred = model(X_test).detach().numpy()
Y_pred = scaler.inverse_transform(Y_pred)
Y_test = scaler.inverse_transform(Y_test)

# 计算误差
mse = np.mean((Y_pred - Y_test)**2)
rmse = np.sqrt(mse)
mape = np.mean(np.abs((Y_pred - Y_test) / Y_test))

print('RMSE: %.5f, MAPE: %.5f%%' % (rmse, mape*100))

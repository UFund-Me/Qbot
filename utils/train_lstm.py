from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 从 Yahoo Finance 获取股票数据
df = yf.download('AAPL', start='2010-01-01', end='2022-03-23')

# 数据预处理
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

# 划分训练集和测试集
train_size = int(len(data_scaled) * 0.8)
train_data = data_scaled[:train_size, :]
test_data = data_scaled[train_size:, :]

# 准备训练数据
seq_len = 30
X_train = []
y_train = []
for i in range(seq_len, len(train_data)):
    X_train.append(train_data[i-seq_len:i, 0])
    y_train.append(train_data[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# 构建LSTM模型
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mse')

# 训练LSTM模型
model.fit(X_train, y_train, epochs=100, batch_size=32)

# 保存LSTM模型
model.save('lstm_model.h5')

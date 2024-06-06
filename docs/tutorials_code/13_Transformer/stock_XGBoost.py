# 导入必要的库
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score

# 读取数据
data = pd.read_parquet('stock_factor.parquet')
data = data.iloc[:10000,:]

# 定义特征和目标变量
M = 20
X = data.iloc[:-M,:].drop(['rtn','ts_code','trade_date'], axis=1)
data['rtn_M'] = data['rtn'].rolling(window=M).sum().fillna(0)
data['label'] = 0
data.loc[data['rtn_M'] > 0 , 'label'] = 1
y = data['label'].iloc[M:]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 转换成 DMatrix 格式
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# 定义 XGBoost 参数
params = { 'max_depth': 3, 'eta': 0.3, 'objective': 'binary:logistic', 'eval_metric': 'auc'}

# 训练模型
model = xgb.train(params, dtrain, num_boost_round=100)

# 测试集预测数据
y_pred = model.predict(dtest)
y_pred = [np.round(value) for value in y_pred]

# 评估结果
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

a = 1
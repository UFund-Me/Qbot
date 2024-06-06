# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 读取数据
# 定义特征和目标变量
M = 20
data = pd.read_parquet('stock_factor.parquet')
data = data.iloc[:10000,:]
X = data.iloc[:-M,:].drop(['rtn','ts_code','trade_date'], axis=1)
y = (data['rtn'].rolling(window=M).sum()).iloc[M:]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义随机森林模型
rf = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42)

# 训练模型
rf.fit(X_train, y_train)

# 分析模型参数
importance = rf.feature_importances_
features = X.columns
indices = np.argsort(importance)[::-1]
for f in range(X.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30, features[indices[f]], importance[indices[f]]))

# 预测结果并可视化
y_pred = rf.predict(X_test)
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.show()

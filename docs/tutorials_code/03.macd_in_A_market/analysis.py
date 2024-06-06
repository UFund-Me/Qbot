import pickle

# 加载保存的结果
f = open('./batch_macd_result.txt', 'rb')
data = pickle.load(f)
f.close()

# 计算
pos = []
neg = []
ten_pos = []
ten_neg = []
for result in data:
    res = data[result]
    if res > 0:
        pos.append(res)
    else:
        neg.append(res)

    if res > 0.1:
        ten_pos.append(result)
    elif res < -0.1:
        ten_neg.append(result)

max_stock = max(data, key=data.get)
print(f'最高收益的股票： {max_stock}, 达到 {data[max_stock]}')
print(f'正收益数量: {len(pos)}, 负收益数量:{len(neg)}')
print(f'+10%数量: {len(ten_pos)}, -10%数量:{len(ten_neg)}')
print(f'收益10%以上的股票: {ten_pos}')

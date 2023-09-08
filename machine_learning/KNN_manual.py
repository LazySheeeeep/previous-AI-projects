import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('wine.data', header=None)

# 数据预处理
X = df.iloc[:, 1:].values
y = df.iloc[:, 0].values
X_mean = np.mean(X, axis=0)  # 特征均值
X_std = np.std(X, axis=0)    # 特征标准差
X = (X - X_mean) / X_std     # 特征标准化


# 定义距离函数
def euclidean_distance(x1, x2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x1, x2)]))


# 定义KNN分类器
class KNN:
    def __init__(self, k):
        self.k = k

    def predict(self, X_train, y_train, X_test):
        y_pred = []
        for x in X_test:
            # 计算测试样本与所有训练样本的距离
            distances = [euclidean_distance(x, x_train) for x_train in X_train]
            # 获取k个最近邻的标签
            k_nearest_labels = [y_train[i] for i in np.argsort(distances)[:self.k]]
            # 对k个最近邻的标签进行投票，选出票数最多的标签作为预测结果
            most_common_label = max(set(k_nearest_labels), key=k_nearest_labels.count)
            y_pred.append(most_common_label)
        return y_pred


# 设置K值范围
k_range = range(1, 31)

# 重复实验得出不同K值下的准确率
accuracies = []
for k in k_range:
    knn = KNN(k)
    y_pred = knn.predict(X_train=X, y_train=y, X_test=X)
    accuracy = sum(y_pred == y) / len(y)
    accuracies.append(accuracy)


# 绘制折线图
plt.plot(k_range, accuracies)
plt.xlabel('K')
plt.ylabel('Accuracy')
plt.xticks(k_range)
plt.show()

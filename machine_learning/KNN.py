import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# 读取数据
columns = ['class', 'alcohol', 'malic_acid', 'ash', 'alcalinity_of_ash',
           'magnesium', 'total_phenols', 'flavanoids',
           'nonflavanoid_phenols', 'proanthocyanins', 'color_intensity',
           'hue', 'od280_od315_of_diluted_wines', 'proline']
data = pd.read_csv('wine.data', names=columns)

# 分割数据
X = data.drop('class', axis=1)
y = data['class']

# 预处理：数据集标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 把数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3)

# 设置K值范围
k_range = range(1, 31)

# 重复实验得出不同K值下的准确率
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    scores.append(knn.score(X_test, y_test))

# 绘制折线图
plt.plot(k_range, scores)
plt.xlabel('K')
plt.ylabel('Accuracy')
plt.xticks(k_range)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# 随机生成实验数据
np.random.seed(0)
X = np.random.rand(100, 1)
y = 2 + 3 * X + np.random.randn(100, 1)

# 添加偏置列
X_b = np.c_[np.ones((100, 1)), X]

# 初始化参数
theta = np.random.randn(2, 1)

# 设置学习率和迭代次数
eta = 0.1
n_iterations = 1000

# 梯度下降算法
for iteration in range(n_iterations):
    gradients = 2/100 * X_b.T.dot(X_b.dot(theta) - y)
    theta = theta - eta * gradients

# 输出参数值
print('theta:', theta)

# 计算均方误差（MSE）
y_predict = X_b.dot(theta)
MSE = np.mean((y - y_predict)**2)
print('MSE:', MSE)

# 绘制拟合直线
X_new = np.array([[0], [1]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta)
plt.plot(X_new, y_predict, 'r')
plt.scatter(X, y)
plt.xlabel('X')
plt.ylabel('y')
plt.show()

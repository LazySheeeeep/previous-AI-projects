from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
import matplotlib.pyplot as plt

# 生成二分类数据
X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)

# 将数据集分成训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 对数据进行标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 创建一个神经网络模型
model = Sequential()
# 添加第一个隐藏层，有10个神经元，使用relu激活函数，输入维度为10
model.add(Dense(units=100, activation='relu', input_dim=10))
# 添加dropout层，随机丢弃50%的神经元
model.add(Dropout(0.5))
# 添加第二个隐藏层，有5个神经元，使用sigmoid激活函数
model.add(Dense(units=50, activation='sigmoid'))
# 添加dropout层，随机丢弃30%的神经元
model.add(Dropout(0.3))
# 添加第三个隐藏层，有10个神经元，使用sigmoid激活函数
model.add(Dense(units=10, activation='sigmoid'))
# 添加dropout层，随机丢弃20%的神经元
model.add(Dropout(0.2))
# 添加输出层，有1个神经元，使用sigmoid激活函数
model.add(Dense(units=1, activation='sigmoid'))

# 编译模型，指定优化算法、损失函数等参数
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 在训练集上训练模型，使用100个epochs和32个batch size
history = model.fit(X_train, y_train, epochs=250, batch_size=32, validation_data=(X_test, y_test))

# 在测试集上评估模型性能
score = model.evaluate(X_test, y_test)
print("Accuracy:", score[1])

# 绘制损失和准确度曲线
fig, ax = plt.subplots(1, 2, figsize=(15, 5))

# 绘制损失曲线
ax[0].plot(history.history['loss'], label='Training Loss')
ax[0].plot(history.history['val_loss'], label='Validation Loss')
ax[0].set_title('Loss')
ax[0].set_xlabel('Epoch')
ax[0].set_ylabel('Loss')
ax[0].legend()

# 绘制准确度曲线
ax[1].plot(history.history['accuracy'], label='Training Accuracy')
ax[1].plot(history.history['val_accuracy'], label='Validation Accuracy')
ax[1].set_title('Accuracy')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Accuracy')
ax[1].legend()

plt.show()
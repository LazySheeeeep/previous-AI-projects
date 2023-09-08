from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB

# 加载Iris数据集
iris = load_iris()
X_iris, y_iris = iris.data, iris.target

# 加载Breast Cancer数据集
breast_cancer = load_breast_cancer()
X_bc, y_bc = breast_cancer.data, breast_cancer.target

# 划分Iris数据集
X_iris_train, X_iris_test, y_iris_train, y_iris_test = \
    train_test_split(X_iris, y_iris, test_size=0.3, random_state=42)

# 划分Breast Cancer数据集
X_bc_train, X_bc_test, y_bc_train, y_bc_test = \
    train_test_split(X_bc, y_bc, test_size=0.3, random_state=42)

# 创建GaussianNB, MultinomialNB和ComplementNB分类器对象
gnb = GaussianNB()
mnb = MultinomialNB()
cnb = ComplementNB()

# 在Iris数据集上进行分类
gnb.fit(X_iris_train, y_iris_train)
mnb.fit(X_iris_train, y_iris_train)
cnb.fit(X_iris_train, y_iris_train)

# 进行测试，得到准确率
iris_acc_gnb = gnb.score(X_iris_test, y_iris_test)
iris_acc_mnb = mnb.score(X_iris_test, y_iris_test)
iris_acc_cnb = cnb.score(X_iris_test, y_iris_test)

print("GaussianNB在Iris数据集上的分类准确率为：{:.2f}%".format(iris_acc_gnb * 100))
print("MultinomialNB在Iris数据集上的分类准确率为：{:.2f}%".format(iris_acc_mnb * 100))
print("ComplementNB在Iris数据集上的分类准确率为：{:.2f}%".format(iris_acc_cnb * 100))

# 在Breast Cancer数据集上进行分类
gnb.fit(X_bc_train, y_bc_train)
mnb.fit(X_bc_train, y_bc_train)
cnb.fit(X_bc_train, y_bc_train)

bc_acc_gnb = gnb.score(X_bc_test, y_bc_test)
bc_acc_mnb = mnb.score(X_bc_test, y_bc_test)
bc_acc_cnb = cnb.score(X_bc_test, y_bc_test)

print("GaussianNB在Breast Cancer数据集上的分类准确率为：{:.2f}%".format(bc_acc_gnb * 100))
print("MultinomialNB在Breast Cancer数据集上的分类准确率为：{:.2f}%".format(bc_acc_mnb * 100))
print("ComplementNB在Breast Cancer数据集上的分类准确率为：{:.2f}%".format(bc_acc_cnb * 100))

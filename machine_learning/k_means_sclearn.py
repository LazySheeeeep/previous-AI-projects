from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 随机生成100个二维数据点
    data = np.random.rand(100, 2) * 100

    # 使用sklearn工具箱实现k-means聚类算法
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)
    labels = kmeans.labels_

    # 获取聚类中心
    centers = kmeans.cluster_centers_

    # 可视化聚类结果和聚类中心
    colors = ['r', 'g', 'b']
    for i in range(len(labels)):
        plt.scatter(data[i, 0], data[i, 1], c=colors[labels[i]])
    for center in centers:
        plt.scatter(center[0], center[1], marker='x', s=200, linewidths=3)
    plt.show()

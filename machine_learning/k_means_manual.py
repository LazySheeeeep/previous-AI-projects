import random
import matplotlib.pyplot as plt


# 计算两个点之间的距离
def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


# 初始化聚类中心
def init_centers(k, data):
    centers = []
    center_indexes = []
    while len(centers) < k:
        index = random.randint(0, len(data) - 1)
        if index not in center_indexes:
            center_indexes.append(index)
            centers.append(data[index])
    return centers


# 分配数据点到最近的聚类中心
def assign_data(data, centers):
    clusters = [[] for _ in range(len(centers))]
    for point in data:
        min_distance = float('inf')
        min_index = -1
        for i in range(len(centers)):
            d = distance(point, centers[i])
            if d < min_distance:
                min_distance = d
                min_index = i
        clusters[min_index].append(point)
    return clusters


# 更新聚类中心
def update_centers(clusters):
    centers = []
    for cluster in clusters:
        if len(cluster) == 0:
            centers.append([0, 0])
        else:
            x = sum([p[0] for p in cluster]) / len(cluster)
            y = sum([p[1] for p in cluster]) / len(cluster)
            centers.append([x, y])
    return centers


# 判断聚类是否稳定
def is_stable(old_centers, new_centers, threshold):
    for i in range(len(old_centers)):
        if distance(old_centers[i], new_centers[i]) > threshold:
            return False
    return True


# k-means聚类算法
def k_means(k, data, threshold=0.1):
    centers = init_centers(k, data)
    while True:
        clusters = assign_data(data, centers)
        new_centers = update_centers(clusters)
        if is_stable(centers, new_centers, threshold):
            break
        centers = new_centers
    return clusters


if __name__ == "__main__":
    # 随机生成100个二维数据点
    data = []
    for i in range(100):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        data.append([x, y])

    # 使用手动实现的k-means聚类算法聚类
    clusters = k_means(3, data)

    # 获取聚类中心
    centers = update_centers(clusters)

    # 可视化聚类结果和聚类中心
    colors = ['r', 'g', 'b']
    for i in range(len(clusters)):
        cluster = clusters[i]
        for point in cluster:
            plt.scatter(point[0], point[1], c=colors[i])
    for center in centers:
        plt.scatter(center[0], center[1], marker='x', s=200, linewidths=3)
    plt.show()

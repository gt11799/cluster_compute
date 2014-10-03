#!usr/bin/env python
'''
compute the errors of hierarchical and kmeans function
'''

from closest_pairs import hierarchical_clustering, kmeans_clustering
from test_alg_project3_viz import load_data_table
import alg_cluster
import matplotlib.pyplot as plt

data_table = load_data_table("CancerData_896.csv")

def compute_distortion(cluster_list):
    error_hie = []
    error_kmeans = []
    for num in range(6, 21):
        clusters_hie = hierarchical_clustering(cluster_list, num)
        clusters_kmeans = kmeans_clustering(cluster_list, num, 5)
    
        error_hie.append(sum([item.cluster_error(data_table) for item in clusters_hie]))
        error_kmeans.append(sum([item.cluster_error(data_table) for item in clusters_kmeans]))
    
    return error_hie, error_kmeans
    
def plot_distortion():
    cluster_list = []
    for line in data_table:
        cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    
    x = range(6, 21)
    (y_hie, y_kmeans) = compute_distortion(cluster_list)
    
    plt.plot(x, y_hie, 'b', label="Hierarchical Clustering")
    plt.plot(x, y_kmeans, 'r', label="K-means Clustering")
    
    plt.legend(loc='best')
    plt.title('Compare the distortion with CancerData_896')
    plt.xlabel("Number of output clusters")
    plt.ylabel("Distortions of the two clusterings")
    
    plt.show()
    
if __name__ == "__main__":
    plot_distortion()
    
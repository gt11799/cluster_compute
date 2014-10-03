#!usr/bin/env python
'''
compare the efficiency of slow_closeset_pairs and fast_closest_pair
'''

from closest_pairs import slow_closest_pairs, fast_closest_pair
import time
import alg_cluster
import random
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    answer = []
    for _ in range(num_clusters):
        cluster = alg_cluster.Cluster(set([]), random.uniform(-1,1), random.uniform(-1,1), 0, 0.0)
        answer.append(cluster)
    return answer
    
def efficiency():
    x = range(2, 201)
    y_slow = []
    y_fast = []
    for item in x:
        clusters_list = gen_random_clusters(item)
        
        t1 = time.time()
        foo = slow_closest_pairs(clusters_list)
        t2 = time.time()
        y_slow.append(t2 - t1)
        
        t1 = time.time()
        bar = fast_closest_pair(clusters_list)
        t2 = time.time()
        y_fast.append(t2 - t1)
        
    return x, y_slow, y_fast
    
def plot_efficiency():
    (x, y_slow, y_fast) = efficiency()
    
    fig = plt.figure(dpi=100)
    plt.plot(x, y_slow, 'b', label="slow_closest_pairs")
    plt.plot(x, y_fast, 'r', label="fast_closest_pair")
    
    plt.legend(loc='best')
    plt.title('Compare the efficiency of the two functions')
    plt.xlabel("Number of clusters")
    plt.ylabel("Time of consuming")
    
    plt.show()
        
    
def test_gen():
    print("test gen_random_clusters", gen_random_clusters(10))
    
if __name__ == "__main__":
    #test_gen()
    plot_efficiency()
    
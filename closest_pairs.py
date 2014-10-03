#!usr/bin/env python
'''
Two algorithm for closest pairs
Take a list of cluster
return the closest pairs
'''

import math
import alg_cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    (d, i, j) = (float('inf'), -1, -1)
    answer = set([])
    length = len(cluster_list)
    for p in range(length-1):
        for q in range(p+1, length):
            (dl, il, jl) = pair_distance(cluster_list, p, q)
            if dl < d:
                answer = set([])
                (d, i, j) = (dl, min(il, jl), max(il, jl))
                answer.add((d, i, j))
            elif d == dl:
                answer.add((dl, min(il, jl), max(il, jl)))
    return answer


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        length = len(horiz_order)
        if length <= 3:
            Q = [cluster_list[idx].copy() for idx in horiz_order]
            (d,i,j) = list(slow_closest_pairs(Q))[0]
            return (d, horiz_order[i], horiz_order[j])
            
        else:
            m = int(length / 2)
            mid = (cluster_list[horiz_order[m-1]].horiz_center() + cluster_list[horiz_order[m]].horiz_center()) / 2
            
            #divide
            Hl = horiz_order[:m]
            Hr = horiz_order[m:]
            Vl = [idx for idx in vert_order if idx in Hl]
            Vr = [idx for idx in vert_order if idx in Hr]
            
            (dl, il, jl) = fast_helper(cluster_list, Hl, Vl)
            (dr, ir, jr) = fast_helper(cluster_list, Hr, Vr)
            (d, i, j) = min((dl, il, jl), (dr, ir, jr))
            
            #merge
            S = [idx for idx in vert_order if abs(cluster_list[idx].horiz_center() - mid) < d]
            length_S = len(S)
            for u in range(length_S-1):
                for v in range(u+1, min(u+4, length_S)):
                    (d,i,j) = min((d,i,j), pair_distance(cluster_list, min(S[u],S[v]), max(S[u],S[v])))
       
        return (d, i, j)
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

    
def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    length = len(cluster_list)
    temp_list = list(cluster_list)
    while length > num_clusters:
        #(d,i,j) = list(slow_closest_pairs(temp_list))[0]
        (d,i,j) = fast_closest_pair(temp_list)
        temp_list[i] = temp_list[i].merge_clusters(temp_list[j])
        temp_list.pop(j)
        
        length = len(temp_list)
    return temp_list

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    length = len(cluster_list)
    temp_list = [(cluster_list[idx].total_population(), idx) for idx in range(length)]
    U = []
    
    #find the cluster with the biggest population
    for _ in range(num_clusters):
        temp = max(temp_list)
        U.append(cluster_list[temp[1]].copy())
        temp_list.remove(temp)
        
    for _ in range(num_iterations):
        answer = [alg_cluster.Cluster(set([]), 0., 0., 0, 0.0) for idx in range(num_clusters)]
        for idx in range(length):
            item = min([(cluster_list[idx].distance(U[idx2]), idx2) for idx2 in range(len(U))])
            answer[item[1]] = answer[item[1]].copy().merge_clusters(cluster_list[idx])
            
        U = list(answer)
        
    return answer
    
def BFClosestPair(cluster_list):
    (d, i, j) = (float('inf'), -1, -1)
    length = len(cluster_list)
    for p in range(length):
        for q in range(p+1, length):
            (d, i ,j) = min((d, i, j), pair_distance(cluster_list, p, q))

    return (d, i, j)

    
def ge_cluster(file_name):
    cluster_list = []
    data_file = open(file_name, 'r')
    lines = data_file.read().split('\r\n')
    data_file.close()
    for line in lines:
        data = line.split(", ")
        cluster = alg_cluster.Cluster(set((data[0],)), float(data[1]), float(data[2]), int(data[3]), float(data[4]))
        cluster_list.append(cluster)
    return cluster_list

def test_BFC():
    cluster_list = ge_cluster('CancerData_111.csv')
    (d,i,j) = BFClosestPair(cluster_list)
    print("test BFClosestPair: ", (d,i,j))
    #print("test BFClosestPair: ", cluster_list[i], cluster_list[j])
    
    
def test_slow():
    cluster_list = ge_cluster('CancerData_24.csv')
    print("test slow_closest_pairs: ", slow_closest_pairs(cluster_list))
    
def test_fast():
    cluster_list = ge_cluster('CancerData_24.csv')
    print("test fast_closest_pairs: ", fast_closest_pair(cluster_list))
    
def test_hierarchical():
    cluster_list = ge_cluster('CancerData_24.csv')
    #print("test hierarchical clustering: ", hierarchical_clustering(cluster_list, 22))
    hierarchical_clustering(cluster_list, 22)

def test_kmeans():
    cluster_list = ge_cluster('CancerData_111.csv')
    print("test kmeans clustering: ", kmeans_clustering(cluster_list, 5, 10))
    
    
if __name__ == "__main__":
    from timeit import Timer
    #print ge_cluster('CancerData_111.csv')
    #test_BFC()
    
    #t1 = Timer("test_slow()", "from __main__ import test_slow")
    #t2 = Timer("test_fast()", "from __main__ import test_fast")
    #print t1.timeit(3)
    #print t2.timeit(3)
    
    test_hierarchical()
    #test_kmeans()

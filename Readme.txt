算法课上的组的计算，根据距离大小，分布在不同地方的点分成组，以population的大小为权值进行合并的计算。

CancerData_*是数据文件，存放着依次是county_code, 坐标（x，y），人口，得癌症的风险。
USA_Counties.png是美国地图，用来绘出癌症风险分布图。

alg_cluster.py定义了一个cluster类，当作计算组合并的对象。

closest_pairs.py是计算组的几个模块，slow和fast方法计算两个最近的点， 以及使用两种方式分组（hierarchical 和 k-means）。

test_alg_project3.py是一个简单的测试模块。需要poc_simpletest.py模块。
test_alg_project3_viz.py是可视化的测试，把计算出的结果画在美国地图上。需要alg_clusters_matplotlib.py模块。

 efficiency_compare.py是用来对比fast和slow模块的效率
 compute_error.py是用来计算误差的。

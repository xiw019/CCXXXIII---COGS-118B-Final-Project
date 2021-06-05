from collections import defaultdict
from random import uniform
from math import sqrt


def distance(a, b):
    dimensions = len(a)
    
    sum_res = 0
    for dimension in range(dimensions):
        difference = (a[dimension] - b[dimension]) ** 2
        sum_res += difference
    return sqrt(sum_res)

def cal_mean(points):

    dimensions = len(points[0])

    new_cluster_centers = []

    for dimension in range(dimensions):
        dim_sum = 0  # dimension sum
        for p in points:
            dim_sum += p[dimension]

        # average of each dimension
        new_cluster_centers.append(dim_sum / float(len(points)))

    return new_cluster_centers

def update_cluster_centers(data_set, assignments):
    
    new_means = defaultdict(list)
    cluster_centers = []
    for assignment, point in zip(assignments, data_set):
        new_means[assignment].append(point)
        
    for points in new_means.values():
        cluster_centers.append(cal_mean(points))

    return cluster_centers
def reassign(data_points, centers):
    
    assignments = []
    for point in data_points:
        shortest = float('inf')  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments





def k_generator(dataset, k):
    
    centers = []
    dimensions = len(dataset[0])
    min_max = defaultdict(int)

    for point in dataset:
        
        for i in range(dimensions):
            val = point[i]
            min_key = 'min_%d' % i
            max_key = 'max_%d' % i
            if min_key not in min_max or val < min_max[min_key]:
                min_max[min_key] = val
            if max_key not in min_max or val > min_max[max_key]:
                min_max[max_key] = val

    for _k in range(k):
        rand_point = []
        for i in range(dimensions):
            min_val = min_max['min_%d' % i]
            max_val = min_max['max_%d' % i]
            
            rand_point.append(uniform(min_val, max_val))

        centers.append(rand_point)

    return centers


def k_means(dataset, k):
    k_points = k_generator(dataset, k)
    assignments = reassign(dataset, k_points)
    old_assignments = None
    centers = None
    while assignments != old_assignments:
        new_centers = update_cluster_centers(dataset, assignments)
        old_assignments = assignments
        assignments = reassign(dataset, new_centers)
        centers = new_centers
    return assignments, centers

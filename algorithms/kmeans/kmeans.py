# By Khaled Abdelaal
# khaled.abdelaal@ou.edu
# Nov, 2020

import math
import random
import copy

# A class for data points
class Point:
    # Constructor for a point
    # takes the following arguments
    #   pid : point id 
    #   vals: the list of values for this data points (one value per dimension)
    #   name: (optional) if we want to specify a name for the data point
    def __init__(self, pid, vals, name=""):
        self.pid = pid
        self.vals = vals
        # assign each point initially to an invalid cluster (-1)
        self.cluster_id = -1
        self.name = name
        # capture the dimensionality of the point
        self.dim = len(self.vals)

    # a setter method for setting the cluster for the point
    # takes the following arguments:
    #   cid : the cluster id
    def setCluster(self, cid):
        self.cluster_id = cid

    # a getter method to get the cluster id to which the point belongs
    def getCluster(self):
        return self.cluster_id

# A class for clusters
class Cluster:
    # Constructor for a cluster
    # takes the following arguments
    #   cid: cluster id
    #   initial_point: the first point in the cluster
    def __init__(self, cid, initial_point):
        self.cid = cid
        self.points = [initial_point]
        
        # Cluster centroid is initially the first point to be added to the cluster
        self.centroid = initial_point.vals

        # A distance dictionary that tracks the distance from each point in the 
        # cluster to the centroid of the cluster
        # keys in this dictionary are point ids, while values are distances
        self.dist = {initial_point.pid: 0}

        # The cluster SSE, initially set to 0
        self.sse = 0.0

    # A method to add a point to the cluster
    # takes the following arguments:
    #   point: the date point to be added to the cluster
    #   dist: the distance from the data point to the current cluster centroid
    def addPoint(self, point, dist):
        self.points.append(point)
        self.dist[point.pid] = dist


    # A method to remove a point from the cluster
    # takes the following arguments:
    #   pid: the id of the point to be removed
    def removePoint(self, pid):
        for point in self.points:
            if point.pid == pid:
                self.points.remove(point)
                self.dist.pop(pid, -1)
                return 1
        return -1

    # A method to find the total number of points within a cluster
    def getNumPoints(self):
        return len(self.points)

    # A method to get the centroid of the cluster
    def getCentroid(self):
        return self.centroid
    
    # A method to set the centroid of the cluster
    # tkaes the following arguments:
    #   newVal : the new value for the centroid (a list of dimension = dim)
    def setCentroid(self, newVal):
        self.centroid = newVal

    # A method to re-calculate the centroid of the cluster
    def adjustCentroid(self):
        new_value = []
        num_points = self.getNumPoints()
        if num_points > 0:
            # goes over all points, one dimension at a time, adds up all values
            # and then finds the mean
            for i in range(self.points[0].dim):
                mean = 0.0
                for j in range(num_points):
                    mean += self.points[j].vals[i]
                new_value.append(mean / num_points)
            self.setCentroid(new_value)

    # A method to calculate SSE for the cluster
    def calculateSSE(self):
        sse = 0
        # goes over the entire distance dictionary and sqaures each distance
        # then adds up all square distances together
        for distance in self.dist.values():
            sse += math.pow(distance, 2)
        return sse

# A class for the K-means clustering algorithm
class Kmeans:
    # Constructor
    # takes the following arguments:
    #   k : number of desired output clusters
    def __init__(self, k):
        self.k = k
        # a list to keep track of all cluster
        self.clusters = []

    
    # A method to find the nearest cluster for a specific data point
    # takes the following argument:
    #   point: the data point
    def findNearestCluster(self, point):

        nearest_cluster_id = 0
        min_dist = 0.0

        if len(self.clusters) < 1:
            print("Error, no clusters found")
            return (-1,-1) 
        

        # get the centroid for cluster 0
        c = self.clusters[0].getCentroid()
        dist = 0.0

        # find Euclidean distance between the point and the centroid of cluster 0
        for i in range(point.dim):
            dist += math.pow(c[i] - point.vals[i], 2)
        dist = math.sqrt(dist)


        # we first assume that the first cluster (clusters[0]) is the closest
        min_dist = dist

        # Now, we go over all centroids of all other clusters 
        # find the distance between each one of them and the data point
        # and capture the minimum distance
        for j in range(1, len(self.clusters)):
            c = self.clusters[j].getCentroid()
            dist = 0.0
            for k in range(point.dim):
                dist += math.pow(c[k] - point.vals[k], 2)
            dist = math.sqrt(dist)
            if dist < min_dist:
                min_dist = dist
                nearest_cluster_id = j
        
        # return both the nearest cluster id and the distance
        # we need to store the distance later in the distance dictionary 
        # for the cluster to calculate SSE
        return (nearest_cluster_id, min_dist)

    
    # the method to do the actual clustering of the data points
    # takes the following arguments:
    #   original_points: the dataset represented as a list of lists
    def do_cluster(self, original_points):

        # make a deep copy of the dataset because we're running over different values of K
        # each run change specific point fields (such as cluster id for example)
        # if we don't deep copy the points before the next K-means run, it will work on dirty
        # points from the previous K-means run
        # we need deepcopy (and not just copy) because each element (point) is an object, so we need 
        # to copy them as well (not just references to them)
        points = copy.deepcopy(original_points)

        if len(points) < self.k:
            print("too few points! terminating!")
            return -1
        
        # choose random centroids for each of the k clusters
        taken_as_centroid = []
        for i in range(self.k):
            while True:
                random_point_idx = random.randint(0, len(points)-1)
                if random_point_idx not in taken_as_centroid:
                    taken_as_centroid.append(random_point_idx)
                    self.clusters.append(Cluster(i, points[random_point_idx]))
                    points[random_point_idx].setCluster(i)
                    break

        
        while True:
            done = True
            # re-assign points to clusters
            for point in points:
                # for each point find the current cluster and the nearest cluster
                # if they don't match, set the point cluster to the new one
                # and remove it from the old one
            
                old_cluster_id = point.getCluster()
                new_cluster_id, dist = self.findNearestCluster(point)
                if (old_cluster_id != new_cluster_id):
                    self.clusters[new_cluster_id].addPoint(point, dist)
                    point.setCluster(new_cluster_id)
                    if (old_cluster_id != -1):
                        self.clusters[old_cluster_id].removePoint(point.pid)
                    done = False
                else:
                    # if the cluster didn't change, we still need to make sure 
                    # that the distance dictionary info is correct (distance might change)
                    if dist != self.clusters[new_cluster_id].dist[point.pid]:
                        self.clusters[new_cluster_id].dist[point.pid] = dist

            # calculate the mean for each cluster
            for cluster in self.clusters:
                cluster.adjustCentroid()
            
            if done:
                break

        final_clusters = [x.getCluster() for x in points]
        
        return final_clusters



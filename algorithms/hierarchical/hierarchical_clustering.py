import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
import math
import pickle
import os

def get_min_distance(a, b, matrix, uniques):
    if type(a) is str:
        a = [uniques.index(a)]
    else:
        a = [uniques.index(i) for i in list(a)]
    if type(b) is str:
        b = [uniques.index(b)]
    else:
        b = [uniques.index(i) for i in list(b)]

    minimum = float("inf")
    min_i = 0
    min_j = 0
    for i in a:
        for j in b:
            if matrix[i, j] < minimum:
                minimum = matrix[i, j]
                min_i = i
                min_j = j

    return minimum, min_i, min_j


def get_max_distance(a, b, matrix, uniques):
    try:
        if type(a) is str:
            a = [uniques.index(a)]
        else:
            a = [uniques.index(i) for i in list(a)]
        if type(b) is str:
            b = [uniques.index(b)]
        else:
            b = [uniques.index(i) for i in list(b)]
    except TypeError:
        print(a, b)
        print(matrix)
        print(uniques)

    maximum = 0
    min_i = 0
    min_j = 0
    for i in a:
        for j in b:
            if matrix[i, j] > maximum:
                maximum = matrix[i, j]
                min_i = i
                min_j = j

    return maximum, min_i, min_j


def sse(data):
    mean = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            mean += matrix[data[i], data[j]] / len(data)

    error = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            error += (matrix[data[i], data[j]] - mean) ** 2
    return error


def hierarchical_clustering(matrix, uniques):
    clusters = uniques
    n = len(clusters)
    c = []
    for i in range(n):
        c.append(clusters[i])

    C = c
    I = n + 1
    linkage = []
    new_clusters = list(clusters)
    while len(C) > 1:
        minimum = float("inf")
        min_i = 0
        min_j = 0
        for i in range(len(C)):
            for j in range(i + 1, len(C)):
                minimum_new, _, _ = get_max_distance(C[i], C[j], matrix, uniques)
                if minimum_new < minimum:
                    minimum = minimum_new
                    min_i = i
                    min_j = j
        new_cluster = []
        if type(C[min_i]) is str:
            new_cluster.append(C[min_i])
        else:
            new_cluster.extend(C[min_i])

        if type(C[min_j]) is str:
            new_cluster.append(C[min_j])
        else:
            new_cluster.extend(C[min_j])

        A = C[min_i]
        B = C[min_j]

        linkage_index_i = new_clusters.index(A)
        linkage_index_j = new_clusters.index(B)

        linkage.append([linkage_index_i, linkage_index_j, minimum, len(new_cluster)])
        print(A)
        print(B)
        print([linkage_index_i, linkage_index_j, minimum, len(new_cluster)])
        print()
        new_clusters.append(new_cluster)

        if min_i > min_j:
            C.pop(min_i)
            C.pop(min_j)
        else:
            C.pop(min_j)
            C.pop(min_i)
        C.append(new_cluster)

        I += 1

    linkage = np.array(linkage)
    print(linkage, )
    return linkage, C, new_clusters


# Reconstruct distance measures into Distance Matrix
def distance_to_matrix():
    size = len(anime_distance['show_1'].dropna().unique())
    matrix = np.identity(size)
    uniques = list(anime_distance['show_1'].dropna().unique())

    for i in range(len(uniques)):
        for j in range(i + 1, len(uniques)):
            show1 = anime_distance.loc[anime_distance['show_1'] == uniques[i]]
            both = show1.loc[show1['show_2'] == uniques[j]]
            matrix[i, j] = both['distance'].iloc[0]
            matrix[j, i] = both['distance'].iloc[0]
    return matrix, uniques


if __name__ == '__main__':
    load = False
    num_anime = 10


    if load:
        (linkage, all_clusters, uniques) = pickle.load(open("../../data/top_" + str(num_anime) + ".p", "rb"))
    else:
        anime_distance = pd.read_csv("../../data/anime_distance_" + str(num_anime) + ".csv")
        matrix, uniques = distance_to_matrix()
        linkage, end_clusters, all_clusters = hierarchical_clustering(matrix, uniques)
        pickle.dump((linkage, all_clusters, uniques), open("../../data/top_" + str(num_anime) + ".p", "wb"))

    plt.figure(figsize=(20, 12))
    plt.title("Popular Anime Dendrogram")
    plt.xlabel("Distance")
    hierarchy.dendrogram(linkage, orientation='left', leaf_font_size=8, labels=np.array(uniques))
    plt.show()
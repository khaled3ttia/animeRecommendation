import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster import hierarchy
from user_recommeder import get_recommendation_hierarchical
import pickle
import os


# Gets the minimum distance between two clusters.
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


# Gets the maximum distance between two clusters
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


# def sse(data):
#     mean = 0
#     for i in range(len(data)):
#         for j in range(i + 1, len(data)):
#             mean += matrix[data[i], data[j]] / len(data)
#
#     error = 0
#     for i in range(len(data)):
#         for j in range(i + 1, len(data)):
#             error += (matrix[data[i], data[j]] - mean) ** 2
#     return error


# Takes in a matrix of distances between elements and a list of the element names.
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
def distance_to_matrix(anime_distance):
    size = len(anime_distance['show_1'].dropna().unique())
    matrix = np.identity(size)
    uniques = list(anime_distance['show_1'].dropna().unique())

    k = 0
    for i in range(len(uniques)):
        for j in range(i + 1, len(uniques)):
            show1 = anime_distance.loc[anime_distance['show_1'] == uniques[i]]
            both = show1.loc[show1['show_2'] == uniques[j]]
            matrix[i, j] = both['distance'].iloc[0]
            matrix[j, i] = both['distance'].iloc[0]
            k += 1
            if k % 1000 == 0:
                print(k)
    return matrix, uniques


# Make a plot of the dendrogram and zoom to the selected show
def plot_tree(group, linkage, all_clusters, uniques, suffix=""):
    plt.figure(figsize=(15, 15))
    plt.title("Popular Anime Dendrogram")
    plt.xlabel("Distance")

    # Make the dendrogram
    dendrogram = hierarchy.dendrogram(linkage, orientation='left', leaf_font_size=8, labels=np.array(uniques))

    # Get the information to zoom the dendrogram
    shows = get_recommendation_hierarchical(group, all_clusters)
    shows.extend(group)

    x, y = [], []
    for c, pi, d in zip(dendrogram['color_list'], dendrogram['icoord'], dendrogram['dcoord']):
        for leg in pi[1:3]:
            i = (leg - 5.0) / 10.0
            if abs(i - int(i)) < 1e-5:
                name = dendrogram['ivl'][int(i)]
                if name in shows:
                    x.append(0.5 * sum(pi[1:3]))
                    y.append(d[1])

    # Zoom the plot to the correct part and make sure the show names display
    plt.ylim(min(x) - 10, max(x) + 10)
    plt.xlim(max(y) + .3, 0)
    plt.tight_layout()

    # Save out the figure
    name = "dendrogram" + str(group) + ".png"
    #location = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))))
    #file_path = location + "\\gui\\" + name
    file_path = "../gui/" + name
    print(file_path)

    #for filename in os.listdir(location + "\\gui\\"):
    for filename in os.listdir('../gui'):
        print(filename)
        if filename.startswith("dendrogram"):
            os.remove("../gui/" + filename)
            #os.remove(location + "\\gui\\" + filename)

    plt.savefig(file_path)
    return name


# Makes a plot of the full dendrogram tree
def plot_full_tree(linkage, all_clusters, uniques):
    plt.figure(figsize=(5, 5))
    plt.title("             Top 25 Popular Anime Dendrogram\nMAX distance")
    plt.xlabel("Distance")
    # Make the dendrogram
    dendrogram = hierarchy.dendrogram(linkage, orientation='left', leaf_font_size=8, labels=np.array(uniques))
    plt.tight_layout()
    plt.savefig("dendrogram.png")


# Load or construct the data needed for the dendogram
def get_dendogram(load=True, num_anime=500):
    if load:
        (linkage, all_clusters, uniques, matrix) = pickle.load(open("../../data/top_" + str(num_anime) + ".p", "rb"))
    else:
        anime_distance = pd.read_csv("../../data/jaccard_anime_distance_" + str(num_anime) + ".csv")
        print("Loaded anime_distance")
        matrix, uniques = distance_to_matrix(anime_distance)
        print("Calculated Distance Matrix")
        linkage, end_clusters, all_clusters = hierarchical_clustering(matrix, uniques)
        print("Clustered Anime")
        pickle.dump((linkage, all_clusters, uniques, matrix), open("../../data/top_" + str(num_anime) + ".p", "wb"))
        print("Saved data")

    return linkage, all_clusters, uniques, matrix


# Calculates the total distance between shows in each cluster and the SSE
def total_distance(a, matrix, uniques):
    try:
        if type(a) is str:
            a = [uniques.index(a)]
        else:
            a = [uniques.index(i) for i in list(a) if i in uniques]
    except TypeError:
        print(a)
        print(matrix)
        print(uniques)

    distance = 0

    for i in range(len(a)-1):
        for j in range(i+1, len(a)):
            distance += matrix[a[i], a[j]]

    mean = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            mean += matrix[a[i], a[j]] / len(a)

    error = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            error += (matrix[a[i], a[j]] - mean) ** 2
    return distance, error


# Gets the SSE of our clusters and genre clusters and plots them.
def evaluation():
    anime_genre = pd.read_csv("../../data/anime_genre.csv").dropna()

    my_clusters_x = []
    my_clusters_y = []
    for cluster in all_clusters:
        d, e = total_distance(cluster, matrix, uniques)
        if type(cluster) == str:
            continue
        if e < 1 * 10 ** 8 and len(cluster) > 1:
            my_clusters_x.append(e)
            my_clusters_y.append(len(cluster))
            print(len(cluster), d, e)
            if e == 0:
                print(cluster)

    genre_set = set()
    for genres in anime_genre['genre']:
        for genre in genres.split(", "):
            genre_set.add(genre)

    genre_set = list(genre_set)

    all_genre_clusters = []
    for genre in genre_set:
        new_genre_cluster = []
        for show, genres in zip(anime_genre['title_english'], anime_genre['genre']):
            if genre in genres.split(", "):
                new_genre_cluster.append(show)
        all_genre_clusters.append(new_genre_cluster)

    genre_clusters_x = []
    genre_clusters_y = []
    for i, cluster in enumerate(all_genre_clusters):
        d, e = total_distance(cluster, matrix, uniques)
        print(genre_set[i], len(cluster), d, e)
        genre_clusters_x.append(e)
        genre_clusters_y.append(len(cluster))

    my_clusters_x = np.array(my_clusters_x)
    my_clusters_y = np.array(my_clusters_y)

    plt.clf()
    plt.scatter(my_clusters_x, my_clusters_y)
    plt.scatter(genre_clusters_x, genre_clusters_y)
    plt.xlim(-100, 10000)
    plt.ylim(0, 25)
    plt.ylabel("Number of Shows in Cluster")
    plt.xlabel("SSE of cluster")
    plt.title("Number of Shows vs SSE")
    plt.legend(["Hierarchical Clusters", "Genre Clusters"])

    plt.figure(2)
    plt.scatter(my_clusters_x, my_clusters_y)
    plt.scatter(genre_clusters_x, genre_clusters_y)
    plt.xlim(-100, 3 * 10 ** 7)
    plt.ylim(0, 200)
    plt.ylabel("Number of Shows in Cluster")
    plt.xlabel("SSE of cluster")
    plt.legend(["Hierarchical Clusters", "Genre Clusters"])
    plt.title("Number of Shows vs SSE")
    plt.show()


# Run this file independently for testing
if __name__ == '__main__':
    linkage, all_clusters, uniques, matrix = get_dendogram(True, 500)

    group = ['Ghost in the Shell']
    plot_full_tree(linkage, all_clusters, uniques)
    evaluation()



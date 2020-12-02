import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from algorithms.kmeans.kmeans import *


def oneTimeProcessing():
    
    # read the three files:

    anime = pd.read_csv('dataset/anime_cleaned.csv')
    userlist = pd.read_csv('dataset/animelists_cleaned.csv')
    user = pd.read_csv('dataset/users_cleaned.csv')

    # removing irrelevant features from each of the three files:

    # from userlist
    cols_to_drop = ['my_watched_episodes', 'my_start_date', 'my_finish_date', 'my_status', 'my_rewatching',
                    'my_rewatching_ep', 'my_last_updated', 'my_tags']

    for col in cols_to_drop:
        userlist = userlist.drop(col, 1)

    # from anime 
    cols_to_drop = ['title_english', 'title_japanese', 'title_synonyms', 'image_url', 'status', 'airing', 
                    'aired_string', 'aired', 'background', 'premiered', 'broadcast', 'related', 'producer',
                    'licensor', 'studio', 'opening_theme', 'ending_theme', 'aired_from_year', 'type', 'genre',
                    'source', 'rating', 'score', 'scored_by', 'duration','episodes', 'rank', 'popularity', 'members', 
                    'favorites', 'duration_min']

    for col in cols_to_drop:
        anime = anime.drop(col, 1)

    # from user 
    cols_to_drop = ['user_watching', 'user_id', 'user_completed', 'user_onhold', 'user_dropped', 'user_plantowatch',
                    'user_days_spent_watching', 'gender', 'location', 'access_rank', 'join_date', 'last_online', 
                    'stats_rewatched', 'stats_episodes', 'birth_date']
    for col in cols_to_drop:
        user = user.drop(col, 1)

    # userlist is huge, would take significant processing power and memory to operate on 
    # so, we sample it using 100K records only

    userlist =  userlist.sample(100000)

    # merge userlist with user
    user_combined = pd.merge(user, userlist, on = ['username', 'username'])

    # We need to keep track of anime shows that the user actually likes
    # we assume that a user likes a show, if he/she gives it a score greater than his/her mean score for all shows 
    # and, we remove all other entries that represent shows that do not fit this criteria
    user_combined = user_combined[user_combined['my_score'] > user_combined['stats_mean_score']]

    # Now, we do not need my_score and stats_mean_score attributes anymore, let's drop them
    user_combined = user_combined.drop('my_score', 1)
    user_combined = user_combined.drop('stats_mean_score', 1)

    # We can merge the resulting dataframe with anime dataframe
    user_anime = pd.merge(user_combined, anime, on=['anime_id', 'anime_id'])

    # Since we need only one row per user, we can re-arrange this dataframe into a cross-table in which the rows 
    # represent usernames and columns represent all anime_id. If a user likes a specific anime, a value of 1 will 
    # be the value of the corresponding anime show 
    user_anime_tab = pd.crosstab(user_anime['username'], user_anime['title'])

    # reduce the dimensionality using Principle Component Analysis 
    from sklearn.decomposition import PCA

    pca = PCA(n_components = 4)
    pca.fit(user_anime_tab)
    pca_instances = pca.transform(user_anime_tab)
    user_anime_reduced = pd.DataFrame(pca_instances)

    feature_cols = list(user_anime_reduced)

    user_anime_reduced['username'] = user_anime_tab.index
    # prepare the final dataset for our k-means implementation
    kmeans_input = user_anime_reduced[feature_cols].values.tolist()

    # Main program starts here


    finalPoints = []
    # store each line as a data point using the Point constructor
    for i in range(len(kmeans_input)):
        finalPoints.append(Point(i, kmeans_input[i]))

    # We have already evaluated different values for k and found that 
    # k = 9 yields the best SSE
    '''
    k_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    sses = []
    # do clustering using different values of K
    for i in range(len(k_values)):
        print("Using a K value of:",k_values[i],"....")
        # initialize Kmeans class
        k_m = Kmeans(k_values[i])
        
        # call the clustering method on the data points
        out_clusters = k_m.do_cluster(finalPoints)

        overall_sse = 0.0
        
        for cluster in k_m.clusters:

            # calculate SSE for each cluster
            cluster_sse = cluster.calculateSSE()

            # print cluster id, centroid, sse, and all point ids
            print("Cluster", cluster.cid)
            print("***********")
            print("Cluster SSE", cluster_sse)
            print("Number of points: ", cluster.getNumPoints())
            overall_sse += cluster_sse
            print("\n---------------------------")
        sses.append(overall_sse)
        print("Overall SSE for K=", k_values[i] , "is:", overall_sse)
        print("====================================================")

    plt.plot(k_values, sses)
    plt.xlabel('Number of clusters (K)')
    plt.ylabel('Sum of Squared Errors (SSE)')
    plt.xticks(k_values)
    plt.savefig('elbow.png')
    '''
    k_m = Kmeans(9)
    out_clusters = k_m.do_cluster(finalPoints)
    user_anime_tab['cluster'] = out_clusters

    c = []

    for i in range(9):
        #c.append(user_anime_tab[user_anime_tab['cluster'] == i].drop('cluster',1).mean())
        c.append(user_anime_tab[user_anime_tab['cluster'] == i].drop('cluster',1).mean())
        c[i].sort_values(ascending=False, inplace=True)
        #print("Cluster" , i)
        #print(c[i][0:10])
        #print(c[i])
        #print("list is", list(c[i]))
        #print("cluster", i)
        #print(c[i].sort_values(ascending=False, inplace=True)[0:10])
        #print(list(c[i]))
    
    return c



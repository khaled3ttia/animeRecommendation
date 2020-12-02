# TODO get the list of shows that the user likes from the backend
#user_likes = getUserLikes()


# a function to return the recommendations
# takes the following arguments:
#       c: the dataframe with final clusters
#       user_likes: a list of shows the user already likes (from frontend)
def getRecommendations(c, user_likes):

    user_likes = ['Paprika', 'Princess Tutu', 'Seto no Hanayome']

    cluster_belongs_to = []
    for anime_history in user_likes:
        score=[]
        for i in range(9):

            if anime_history in c[i]:
                #print("Found in cluster", i)
                score.append(c[i][anime_history])
            else:
                print("Anime name not found in the db")
                break
        anime_belongs_to = max( (val, idx) for idx, val in enumerate(score))[1]
        if anime_belongs_to not in cluster_belongs_to:
            cluster_belongs_to.append(max( (val, idx) for idx, val in enumerate(score))[1])

    #print("Clusters matched: " , cluster_belongs_to)
    #print("Other anime shows you might be interested in: ")

    recommendations = set()
    for target_cluster in cluster_belongs_to:
        anime_shows = c[target_cluster][0:10].index.format()
        for recommended_anime in anime_shows:
            recommendations.add(recommended_anime)
    
    return recommendations
    

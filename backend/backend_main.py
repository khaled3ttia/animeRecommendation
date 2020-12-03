from flask import Flask, render_template, request
import os
import pickle
from user_recommeder import getRecommendations, get_recommendation_hierarchical

app = Flask(__name__)
file_to_render = "new.html"
#app.static_folder = os.path.dirname(os.getcwd())+"\\gui"
#app.template_folder = os.path.dirname(os.getcwd())+"\\gui"
app.static_folder = "../gui"
app.template_folder = "../gui"

@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.values)
    favorite_anime = [request.form.get("fav-anim")]
    clustering_type = request.form.get("algo")

    print(favorite_anime)
    if favorite_anime != [None]:
        if clustering_type == "kmeans":
            recommendations = getRecommendations(c, favorite_anime)
            # for now let's just print the recommendations
            print("You might also be interested in the following shows")
            for show in recommendations:
                print(show)
        else:
            recommendations = get_recommendation_hierarchical(favorite_anime, all_clusters)
            print("You might also be interested in the following shows")
            for show in recommendations:
                print(show)

        return render_template(file_to_render, data=recommendations)
    return render_template(file_to_render)


if __name__ == '__main__':
    print(os.getcwd())
    c = pickle.load(open("../data/clusters.p", "rb"))
    (linkage, all_clusters, uniques) = pickle.load(open("../data/top_250.p", "rb"))
    app.run()

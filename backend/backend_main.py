from flask import Flask, render_template, request
import os
import pickle
from user_recommeder import getRecommendations, get_recommendation_hierarchical
import algorithms.hierarchical.hierarchical_clustering as hc

app = Flask(__name__)
file_to_render = "new.html"
app.static_folder = "../gui"
app.template_folder = "../gui"


@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.values)
    favorite_anime = request.form.getlist("animeList")
    clustering_type = request.form.get("algo")

    print(favorite_anime)
    if favorite_anime:
        # Run this in a try catch loop to catch errors when anime are missing.
        try:
            # Get the recommendations for that anime
            if clustering_type == "kmeans":
                recommendations = getRecommendations(c, favorite_anime)
                image = None
            else:
                recommendations = get_recommendation_hierarchical(favorite_anime, all_clusters)
                image = []
                for i, item in enumerate(favorite_anime):
                    if item in all_clusters:
                        image.append(hc.plot_tree([item], linkage, all_clusters, uniques, i))
        except (TypeError, ValueError):
            print("Error")
            recommendations = None
            image = None

        if recommendations is not None:
            # for now let's just print the recommendations
            print("You might also be interested in the following shows")
            for show in recommendations:
                print(show)

            if image is not None:
                return render_template(file_to_render, data=recommendations, img=image)
            else:
                return render_template(file_to_render, data=recommendations)

    return render_template(file_to_render)


if __name__ == '__main__':
    print(os.getcwd())
    c = pickle.load(open("../data/clusters.p", "rb"))
    (linkage, all_clusters, uniques) = pickle.load(open("../data/top_250.p", "rb"))
    app.run()

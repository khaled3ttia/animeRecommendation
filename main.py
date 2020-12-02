from processing.proc import *
from backend.user import *

# Executed only once during the lifetime of the application
c = oneTimeProcessing()

# TODO replace this with a dynamic input (backend from frontend)
# user_likes = getUserInput()

user_likes = ['Paprika', 'Princess Tutu', 'Seto no Hanayome']

# TODO this function to be called when the user presses submit
recommendations = getRecommendations(c, user_likes)

# TODO send the recommendations back to the UI


# for now let's just print the recommendations
print("You might also be interested in the following shows")

for show in recommendations:
    print(show)

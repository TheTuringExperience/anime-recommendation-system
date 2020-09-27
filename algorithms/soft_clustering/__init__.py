import os
from typing import List
import pickle

#A dict where the keys are the anime codes and the values are a one_hot vector encoding the genres the anime belongs to
animes_genres = pickle.load(open("./algorithms/soft_clustering/anime_genres.pickle", "rb"))
name_to_code = pickle.load(open("./algorithms/soft_clustering/name_to_code.pickle", "rb"))

def soft_clustering_recommendator(anime_name: str) -> List[int]:
    #get the one_hot encoded representation of the genres
    code = name_to_code.get(anime_name, 0)
    genres = animes_genres.get(code)[0]
    #get the index in the one_hot vector for each genre
    indexes = [i for i in range(0, len(genres)) if genres[i] == 1]
    top_recommendations = []
    #Iterate over all the animes
    for key, values in animes_genres.items():
        #this counts how many genres the anime this anime and the anime we want the recommendations for have in common
        similarity = sum(values[0][indexes])
        #This first is is just to make sure we don't include the anime itself
        if key != code:
            #if the list of recommendations has less than five items insert anything and continue on
            if len(top_recommendations) < 5:
                top_recommendations.append([key, similarity])
                continue
            # if the current anime has more genres in common than another one in the \
            # top_recommendations list then replace it
            for idx, recommendation in enumerate(top_recommendations):
                if similarity > recommendation[1]:
                    top_recommendations[idx] = [key, similarity]
                    break

    return [recom[0] for recom in top_recommendations]

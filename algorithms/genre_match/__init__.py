import os
from typing import List

import numpy as np
import pandas as pd
import pickle

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import jaccard_score

# TODO: Fix pathing in the future based on these guidelines - http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
# anime_genres_df = pd.read_pickle("./algorithms/genre_match/anime_genres_df.pkl")

# full_df = pd.read_pickle("./algorithms/genre_match/full_df.pkl")
all_recommendations_dict = {}
with open('./algorithms/genre_match/genre_match_recs.pickle', 'rb') as handle:
    all_recommendations_dict = pickle.load(handle)

weight_dict = {"score":0.1, "popularity":0.1, "members":0.05, "scored_by":0.05, "similarity":0.7}

def genre_match(anime_code: int, n_recommendations:int) -> List[int]:
    try:
        return all_recommendations_dict[float(anime_code)][0:n_recommendations]

    except Exception as e:
        return []


def genre_match_randomanime(anime_code: int, page_number:int, page_size:int = 50):
    try:
        offset = page_size * (page_number - 1)
        recommendations = all_recommendations_dict[float(anime_code)][offset:page_number*page_size]
        return recommendations, []
        
    except Exception as e:
        print("genre_match ", e)
        return [], []

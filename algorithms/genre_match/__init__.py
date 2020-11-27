import os
from typing import List

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import jaccard_score
from utils import preprocess_names, get_anime_code_from_name

# TODO: Fix pathing in the future based on these guidelines - http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
anime_genres_df = pd.read_pickle("./algorithms/genre_match/anime_genres_df.pkl")
full_df = pd.read_pickle("./algorithms/genre_match/full_df.pkl")

def genre_match_recommender(anime_name: str) -> List[int]:
    try:
        df = anime_genres_df.copy()
        anime_code = get_anime_code_from_name(anime_name)
        anime_data = df.loc[anime_code]
        df.drop(anime_code, axis=0, inplace=True)  # Drop the anime to make sure it's not recommended

        df["similarity"] = df.apply(lambda x: jaccard_score(x.values, anime_data.values), axis = 1)
        df = pd.concat([df,full_df.score], axis=1)

        df = df.sort_values(by=["similarity", "score"], ascending=False)
        recommendations = df.iloc[:5].index.tolist()    
        return recommendations
    except Exception as e:
        print(e)    
        return []

import os
from typing import List

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import jaccard_score

# TODO: Fix pathing in the future based on these guidelines - http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
# anime_genres_df = pd.read_pickle("./algorithms/genre_match/anime_genres_df.pkl")
full_df = pd.read_pickle("./algorithms/genre_match/full_df.pkl")

def calculate_ranking_score(row, config_dict):
    score = row['score'] * config_dict['score']
    popularity = row['popularity'] * config_dict['popularity']
    members = row['members'] * config_dict['members']
    scored_by = row['scored_by'] * config_dict['scored_by']
    similarity = row['similarity'] * config_dict['similarity']
    return score + popularity + members + scored_by + similarity

def genre_match_recommender(anime_code: int, n_recommendations:int, weight_dict) -> List[int]:
    try:
        df = full_df.copy()        
        anime_data = df.loc[anime_code]
        df.drop(anime_code, axis=0, inplace=True)  # Drop the anime row to make sure it's not recommended

        df["similarity"] = df[anime_code]
        cols_to_keep = ["score", "popularity", "members", "scored_by", "similarity"]
        df = df[cols_to_keep]
        df['ranking_score'] = df.apply(calculate_ranking_score, axis=1, args=(weight_dict,))

        df = df.sort_values(by=["ranking_score"], ascending=False)
        recommendations = df.iloc[:n_recommendations].index.tolist()    
        return recommendations

    except Exception as e:
        print(e)    
        return []

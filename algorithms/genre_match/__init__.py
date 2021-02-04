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

def calculate_ranking_score(row, config_dict):
    score = row['score'] * config_dict['score']
    popularity = row['popularity'] * config_dict['popularity']
    members = row['members'] * config_dict['members']
    scored_by = row['scored_by'] * config_dict['scored_by']
    similarity = row['similarity'] * config_dict['similarity']
    return score + popularity + members + scored_by + similarity

def genre_match(anime_code: int, n_recommendations:int): 
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

<<<<<<< HEAD
def genre_match_randomanime(anime_code: int, page_number:int, page_size: int = 50):
    try:
        df = full_df.copy()        
        anime_data = df.loc[anime_code]
        df.drop(anime_code, axis=0, inplace=True)  # Drop the anime row to make sure it's not recommended

        df["similarity"] = df[anime_code]
        cols_to_keep = ["score", "popularity", "members", "scored_by", "similarity"]
        df = df[cols_to_keep]
        df['ranking_score'] = df.apply(calculate_ranking_score, axis=1, args=(weight_dict,))

        df = df.sort_values(by=["ranking_score"], ascending=False)
        offset = page_size * (page_number - 1)
        recommendations = df.iloc[offset:page_number*page_size].index.tolist()
        return recommendations
        
=======
def genre_match_recommender(anime_code: int, n_recommendations:int, weight_dict) -> List[int]:
    try:
        return all_recommendations_dict[float(anime_code)][0:n_recommendations]

>>>>>>> e12a5228287d048868cdcb4064c4e55242bc039d
    except Exception as e:
        print(e)    
        return []

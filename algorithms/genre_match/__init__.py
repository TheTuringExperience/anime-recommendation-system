import os
from typing import List

import numpy as np
import pandas as pd

from utils import preprocess_names

relevant_fields = ["code", "show_titles", "genres", "premiered", "score"]

# TODO: Fix pathing in the future based on these guidelines - http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
anime_genres_df = pd.read_pickle("./algorithms/genre_match/anime_genres_df.pkl")[relevant_fields]
anime_genres_df["name"] = [names_l[0] for names_l in preprocess_names(anime_genres_df["show_titles"].to_list())]

def genre_match_recommendator(anime_name: str, ranking_parameter: str) -> List[int]:
    try:
        df = anime_genres_df.copy()
        anime_data = df.loc[df["name"] == anime_name]
        df.drop(anime_data.index, axis=0, inplace=True)  # Drop the anime to make sure it's not recommended

        df["similarity"] = df.genres.map(lambda x: np.dot(x, anime_data["genres"].values[0]))
        df = df.sort_values(by=[str(ranking_parameter), "similarity"], ascending=False)
        recommendations = df.iloc[:5].code.tolist()    
        return recommendations
    except Exception as e:
        print(e)    
        return []

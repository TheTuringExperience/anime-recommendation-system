import os
from typing import List

import numpy as np
import pandas as pd

relevant_fields = ["code", "show_titles", "genres", "premiered", "score"]

# TODO: Fix pathing in the future based on these guidelines - http://python-notes.curiousefficiency.org/en/latest/python_concepts/import_traps.html
anime_genres_df = pd.read_pickle("./algorithms/soft_clustering/anime_genres_df.pkl")[relevant_fields]

def soft_clustering_recommendator(anime_code: int, raking_parameter: str, n_recommendations: int) -> List[int]:
    try:
        df = anime_genres_df.copy(deep=True)
        anime_data = df.loc[df["code"] == anime_code]
        df.drop(anime_data.index, axis=0, inplace=True) #Drop the anime to make sure it's not recommended

        df["similarity"] = df.genres.map(lambda x: np.dot(x, anime_data["genres"].values[0]))
        df = df.sort_values(by=[str(raking_parameter), "similarity"], ascending=False)
        recommendations = df.iloc[:n_recommendations].code.tolist()    
        return recommendations

    except Exception as e:
        print(e)    
        return []

import os
from typing import List
import numpy as np
import pandas as pd

anime_genres_df = pd.read_pickle("./algorithms/soft_clustering/anime_genres_df.pkl")

def soft_clustering_recommendator(anime_name: str) -> List[int]:
    try:
        df = anime_genres_df.copy()
        anime_data = df.loc[anime_genres_df["name"] == anime_name]
        df["similarity"] = df.genres.map(
            lambda x: np.dot(x, anime_data["genres"].values[0]))
        df = df.sort_values(by=["premiered", "similarity"], ascending=False)
        recommendations = df.iloc[:5].code.tolist()    
        return recommendations
    except:    
        return []
import os
from typing import List

import numpy as np
import pandas as pd

characters_df = pd.read_pickle("./algorithms/character_match/characters_df.pkl")


def character_match_recommender(anime_code: int, n_recommendations: int):
    try:
        df = characters_df.copy(deep=True)
        characters_data = df.loc[df["mal_code"] == anime_code]
        # Drop the anime to make sure it's not recommended
        df.drop(characters_data.index, axis=0, inplace=True)

        df["similarity"] = df.character_tags.map(lambda x: np.dot(x, characters_data["character_tags"].to_numpy()[0]))
        df = df.sort_values(by=["similarity"], ascending=False)
        #Drop duplicated anime
        df.drop_duplicates(subset=["mal_code"], inplace=True)

        recommendations = df.iloc[:n_recommendations].mal_code.tolist()
        return recommendations

    except Exception as e:
        print(e)
        return []


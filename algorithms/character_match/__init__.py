import os
from typing import List

import numpy as np
import pandas as pd

characters_df = pd.read_pickle("./algorithms/character_match/characters_df.pkl")


def character_match(anime_code: int, n_recommendations:int):
    try:
        df = characters_df.copy(deep=True)
        characters_data = df.loc[df["mal_code"] == anime_code]
        # Drop the anime to make sure it's not recommended
        df.drop(characters_data.index, axis=0, inplace=True)

        df["similarity"] = df.main_characters_tags.map(lambda x: np.dot(x, characters_data["main_characters_tags"].to_numpy()[0]))
        df = df.sort_values(by=["similarity"], ascending=False)
        #Drop duplicated anime
        df.drop_duplicates(subset=["mal_code"], inplace=True)

        recommendations = df.iloc[:n_recommendations].mal_code.tolist()
        return recommendations

    except Exception as e:
        print(e)
        return [] 

def character_match_randomanime(anime_code: int, page_number: int, page_size: int = 50):
    try:
        df = characters_df.copy(deep=True)
        characters_data = df.loc[df["mal_code"] == anime_code]
        # Drop the anime to make sure it's not recommended
        df.drop(characters_data.index, axis=0, inplace=True)

        df["similarity"] = df.main_characters_tags.map(lambda x: np.dot(x, characters_data["main_characters_tags"].to_numpy()[0]))
        df = df.sort_values(by=["similarity"], ascending=False)
        #Drop duplicated anime
        df.drop_duplicates(subset=["mal_code"], inplace=True)

        offset = page_size * (page_number - 1)
        recommendations = df.iloc[offset:page_number*page_size].mal_code.tolist()
        return recommendations

    except Exception as e:
        print(e)
        return []


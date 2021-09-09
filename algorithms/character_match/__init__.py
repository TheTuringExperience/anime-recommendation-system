import os

import numpy as np
import pandas as pd
from joblib import load

characters_df = pd.read_pickle("./algorithms/character_match/characters_df.pkl")
character_tags_encoder = load("./algorithms/character_match/character_tags_encoder.joblib")

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
        explanations = [generate_explanation(anime_code, recommendation) for recommendation in recommendations]        
        return recommendations, explanations

    except Exception as e:
        print("character_match ", e)
        return [], []


def generate_explanation(first_show_code: int, second_show_code: int):
    characters_first_show = characters_df[characters_df.mal_code == first_show_code]
    characters_second_show = characters_df[characters_df.mal_code == second_show_code]
    matched = set()
    max_sim = 2
    similarities = dict() 
    for idx1, row1 in characters_first_show.iterrows():
        for idx2, row2 in characters_second_show.iterrows():
            mul = np.multiply(row1["character_tags"], row2["character_tags"])            
            sim = sum(mul)
            # ensure that there are not repeated characters and that the sim is always max(2, argmax(sim))
            if sim >= max_sim and row1["name"] not in matched:
                matched.add(row1["name"])
                max_sim = sim                
                similarities[f"{row1['name']}:{row2['name']}"] = character_tags_encoder.inverse_transform(np.array([mul]))    
    return similarities

# if __name__ == "__main__":
#     print(character_match_randomanime(1, 1))

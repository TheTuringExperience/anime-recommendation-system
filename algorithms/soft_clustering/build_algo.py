""" Creates the files needed to run the soft_culstering recommender algorithm"""

import os
import re
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

anime_data_path = "../../data/anime_data.csv"

animes_df = pd.read_csv(anime_data_path, encoding="utf-8")[["name", "code", "premiered", "genres"]]

#create a list of genres using the "genres" column in the animes_df
genres = list({genre  for genres_list in animes_df.genres.tolist() 
                        for genre in genres_list.split(";")})

#create a one_hot encoded representation of each genre
one_hot = OneHotEncoder(handle_unknown="ignore")
one_hot.fit([[genre] for genre in genres])

def get_genres_vector(genres_str: str):
    """returns the sum of the one-hot representations of the genres"""
    genres = genres_str.split(";")
    genres_vector = sum([one_hot.transform([[genre]]).toarray() for genre in genres])[0]
    return genres_vector

def main():
    animes_df["genres"] = animes_df.genres.apply(get_genres_vector)
    #process the anime names to remove underscores
    animes_df["name"] = animes_df.name.apply(lambda x: re.sub(r"\s\s+", " ", re.sub(r"[\_+-]", " ", x)))

if __name__ == "__main__":
    main()
    #save the dict as a binary pickle file
    animes_df.to_pickle("./anime_genres_df.pkl")

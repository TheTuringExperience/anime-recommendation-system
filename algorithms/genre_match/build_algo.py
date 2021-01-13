""" Creates the files needed to run the genre_match recommender algorithm"""

import os
import re
import pickle

import numpy as np
import pandas as pd
import datetime as dt

from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.metrics.pairwise import pairwise_distances

anime_data_path = "../../data/anime_data.csv"

# relevant_fields = ["show_titles", "score", "code", "premiered", "genres", "popularity", "members","scored_by","type","rating"]
relevant_fields = ["show_titles", "score", "code", "premiered", "genres", "popularity", "members","scored_by"]
animes_df = pd.read_csv(anime_data_path, encoding="utf-8")[relevant_fields]

season_to_month = {"Winter": "01", "Spring": "04", "Summer": "07", "Fall": "10"}

def convert_to_date(anime_season: str):
    if isinstance(anime_season, str) and anime_season != "Not available":
        season, year = anime_season.split(" ")
        month = season_to_month[season]
        airing_date = "/".join(["01", month, year])
        return airing_date
    return None

def genres_to_array(genres_str: str):
    return genres_str.split(';')

def main():
    initial_df = animes_df.copy()
    initial_df['genres_array'] = initial_df.genres.apply(genres_to_array) 
    initial_df["premiered"] = initial_df.premiered.apply(convert_to_date) 
    initial_df["premiered"] = pd.to_datetime(initial_df['premiered']).dt.date
    initial_df['time_diff'] = dt.datetime.now().date() - initial_df['premiered']
    initial_df = initial_df.set_index('code')   

    # normalize values
    columns_to_scale = ["score", "popularity", "members", "scored_by"]
    min_max_scaler = MinMaxScaler()
    initial_df[columns_to_scale] = min_max_scaler.fit_transform(initial_df[columns_to_scale])
    # print(initial_df.head())

    mlb = MultiLabelBinarizer()
    binary_df = pd.DataFrame(mlb.fit_transform(initial_df['genres_array']),columns=mlb.classes_, index=initial_df.index)
    # print(binary_df.head())

    jac_sim = 1 - pairwise_distances(binary_df, metric = "hamming")
    jac_sim = pd.DataFrame(jac_sim, index=binary_df.index, columns=binary_df.index)
    # print(jac_sim.head())
    # binary_df.to_pickle("./anime_genres_df.pkl")

    output_df = pd.concat([initial_df, jac_sim], axis=1)
    # print(output_df.head())
    output_df.to_pickle("./full_df.pkl")

if __name__ == "__main__":
    main()

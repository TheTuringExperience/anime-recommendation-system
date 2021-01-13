""" Takes the data for the shows in ../data/anime_codes_by_genre and saves them in ../data/anime_codes.csv removing repeated shows"""

import os
import pandas as pd

anime_codes_dir = "../data/anime_codes_by_genre"

codes_df = pd.DataFrame()

for csv_file in os.listdir(anime_codes_dir):
    if codes_df.empty:
        codes_df = pd.read_csv(os.path.join(anime_codes_dir, csv_file))
    else:
        genre_df = pd.read_csv(os.path.join(anime_codes_dir, csv_file))
        codes_df = codes_df.append(genre_df)

codes_df = codes_df[codes_df["rating"] >= 6.5]
codes_df.drop_duplicates(subset=['code'], inplace=True)

codes_df.to_csv("../data/anime_codes.csv", index = False)

""" Creates a single .csv file with all anime codes and no overlap """

import os
import pandas as pd

working_dir = os.getcwd()
anime_codes_dir = os.path.join(working_dir, "anime_codes_by_genre")

codes_df = pd.DataFrame()

for csv_file in os.listdir(anime_codes_dir):
    if codes_df.empty:
        codes_df = pd.read_csv(os.path.join(anime_codes_dir, csv_file))
    else:
        genre_df = pd.read_csv(os.path.join(anime_codes_dir, csv_file))
        codes_df = codes_df.append(genre_df)

codes_df = codes_df[codes_df["rating"] >= 6.5]
codes_df.drop_duplicates(subset=['code'], inplace=True)

codes_df.to_csv(os.path.join(working_dir, "anime_codes.csv"), index=False)

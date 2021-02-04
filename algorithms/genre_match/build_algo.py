""" Creates the files needed to run the genre_match recommender algorithm"""

import os
import re
import pickle

import numpy as np
import pandas as pd
import datetime as dt

from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
from sklearn.metrics.pairwise import pairwise_distances

anime_data_path = "../../data/anime_data_randomanime.csv"

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

def calculate_ranking_score(row, config_dict):
    score = row['score'] * config_dict['score']
    popularity = row['popularity'] * config_dict['popularity']
    members = row['members'] * config_dict['members']
    scored_by = row['scored_by'] * config_dict['scored_by']
    similarity = row['similarity'] * config_dict['similarity']
    return score + popularity + members + scored_by + similarity

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
    # output_df.to_pickle("./full_df.pkl")

    df = output_df.copy()    
    anime_codes = output_df.index.values.tolist() 
    all_recommendations_dict = {}
    weight_dict={"score":0.1, "popularity":0.1, "members":0.05, "scored_by":0.05, "similarity":0.7}
    count = 0

    for anime_code in anime_codes: 
        df["similarity"] = df[anime_code]
        df['ranking_score'] = df.apply(calculate_ranking_score, axis=1, args=(weight_dict,))

        df = df.sort_values(by=["ranking_score"], ascending=False)
        recommendations = df.iloc[1:].index.tolist()    
        all_recommendations_dict[anime_code] = recommendations

        count += 1
        if (count % 100 == 0): print('Processed: {}'.format(count))
        
    with open('genre_match_recs.pickle', 'wb') as handle:
        pickle.dump(all_recommendations_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    print('Finished: {}'.format(len(all_recommendations_dict)))

if __name__ == "__main__":
    main()

    # # Testing
    # anime_code = 11757
    # n_recommendations = 15

    # with open('genre_match_recs.pickle', 'rb') as handle:
    #     all_recommendations_dict = pickle.load(handle)
    #     print(all_recommendations_dict[float(anime_code)][0:n_recommendations])

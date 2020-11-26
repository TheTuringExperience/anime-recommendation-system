from sklearn.metrics import ndcg_score
import numpy as np
import pandas as pd
import os
import sys

from algorithms.soft_clustering import soft_clustering_recommendator
from recommendations_manager import obtain_recommendations, obtain_random_recommendations
from utils import get_anime_code_from_name

anime_name = 'cowboy bebop'
anime_code = get_anime_code_from_name(anime_name)
print("current anime: {}".format(anime_code))

data = pd.read_csv('data/recommendations/{}.txt'.format(anime_code), sep=",", header=None)
data.columns = ["mal_id", "relevance", "name"]

def print_matches(recs):
    for item in recs:
        curr_code = item['code']
        if (curr_code in data.mal_id.values):
            match = data.loc[data['mal_id'] == curr_code].iloc[0]
            print("item: {}, match_name: {}, rec_count: {}".format(curr_code, match['name'], match['relevance']))


recs = obtain_recommendations(anime_name)

synopsis_recs = recs["similar_synopsis"]
print_matches(synopsis_recs)

review_recs = recs["similarly_described"]
print_matches(review_recs)

hot_recs = recs["hot"]
print_matches(hot_recs)

popular_recs = recs["beloved"]
print_matches(popular_recs)



true_relevance = np.asarray([[10, 0, 0, 1, 5]])
scores = np.asarray([[.1, .2, .3, 4, 70]])
print(ndcg_score(true_relevance, scores))
from sklearn.metrics import ndcg_score
import numpy as np
import pandas as pd
import os
import sys

from algorithms.soft_clustering import soft_clustering_recommendator
from recommendations_manager import obtain_recommendations, obtain_random_recommendations
from utils import get_anime_code_from_name

anime_name = 'vinland saga'
anime_code = get_anime_code_from_name(anime_name)
print(anime_code)

recs = obtain_recommendations(anime_name)
print(recs)

synopsis_recs = recs["similar_synopsis"]
print(synopsis_recs)

data = pd.read_csv('data/recommendations/{}.txt'.format(anime_code), sep=",", header=None)
data.columns = ["mal_id", "relevance", "name"]
print(data.head())


true_relevance = np.asarray([[10, 0, 0, 1, 5]])
scores = np.asarray([[.1, .2, .3, 4, 70]])
print(ndcg_score(true_relevance, scores))
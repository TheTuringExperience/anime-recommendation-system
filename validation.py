from sklearn.metrics import ndcg_score
import numpy as np
import pandas as pd
import os
import sys

from algorithms.soft_clustering import soft_clustering_recommendator

data = pd.read_csv('../../data/recommendations/1.txt', sep=",", header=None)
data.columns = ["mal_id", "relevance", "name"]

data.head()


true_relevance = np.asarray([[10, 0, 0, 1, 5]])
scores = np.asarray([[.1, .2, .3, 4, 70]])
ndcg_score(true_relevance, scores)
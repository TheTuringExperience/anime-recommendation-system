from algorithms.word2vec import similarity_recommendator
from algorithms.soft_clustering import soft_clustering_recommendator

recommender_algorithms = {
    "similarity_search": similarity_recommendator,
    "soft_clustering": soft_clustering_recommendator}

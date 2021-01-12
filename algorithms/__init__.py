from algorithms.word2vec import similarity_recommendator
from algorithms.soft_clustering import soft_clustering_recommendator
from algorithms.synopsis_similarity import synopsis_similarity_recommender
from algorithms.genre_match import genre_match_recommender
from algorithms.character_match import character_match_recommender
from algorithms.random import random_recommender

recommender_algorithms = {
    "similarity_search": similarity_recommendator,
    "soft_clustering": soft_clustering_recommendator,
    "synopsis_similarity": synopsis_similarity_recommender,
    "genre_match": genre_match_recommender,
    "character_match": character_match_recommender,
    "random": random_recommender}

from algorithms.word2vec import review_similarity, review_similarity_randomanime 
from algorithms.soft_clustering import soft_clustering, soft_clustering_new_randomanime, soft_clustering_popularity_randomanime
from algorithms.synopsis_similarity import synopsis_similarity, synopsis_similarity_randomanime
from algorithms.genre_match import genre_match, genre_match_randomanime
from algorithms.character_match import character_match, character_match_randomanime
from algorithms.random import random_recommender

recommender_algorithms = {
    "review_similarity": review_similarity,
    "soft_clustering": soft_clustering,
    "synopsis_similarity": synopsis_similarity,
    "genre_similarity": genre_match,
    "character_similarity": character_match,
    "random": random_recommender
} 

recommender_algorithms_randomanime = {
    "review_similarity": review_similarity_randomanime,
    "synopsis_similarity": synopsis_similarity_randomanime,
    "genre_similarity": genre_match_randomanime,
    "character_similarity": character_match_randomanime,
    "soft_clustering_new": soft_clustering_new_randomanime,
    "soft_clustering_popularity": soft_clustering_popularity_randomanime
}
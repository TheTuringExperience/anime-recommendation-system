""" It's in charge of managing communication between the api and the recommerder algoriths """

import os
import pickle
from collections import defaultdict
from typing import List, Dict

from numpy.random import choice
import pandas as pd
import networkx as nx

from utils import preprocess_names
from algorithms import * 

anime_info_df = pd.read_csv("data/anime_data.csv", encoding="utf-8")
anime_info_df["name"] = [names_l[0] for names_l in preprocess_names(anime_info_df["show_titles"].to_list())]
anime_info_df["genres"] = anime_info_df["genres"].apply(lambda s: s.split(";"))

G = nx.readwrite.gpickle.read_gpickle("recommendations_manager/graph.pkl")

relevant_fields = ['show_titles', 'code', 'score', 'image_url', 'synopsis', 'premiered', 'type', 'genres']

def obtain_recommendations(anime_code: int, n_recommendations: int) -> Dict[str, List[str]]:
    recom = defaultdict(list)    
    
    #get the codes of the recommendations from the algorithms and then get the info about them
    similar = get_info_from_code(recommender_algorithms["similarity_search"](anime_code, n_recommendations), anime_code)
    hot = get_info_from_code(recommender_algorithms["soft_clustering"](anime_code, "premiered", n_recommendations), anime_code)
    beloved = get_info_from_code(recommender_algorithms["soft_clustering"](anime_code, "score", n_recommendations), anime_code)
    similar_synopsis = get_info_from_code(recommender_algorithms["synopsis_similarity"](anime_code, n_recommendations), anime_code)
    genre_match = get_info_from_code(recommender_algorithms["genre_match"](anime_code, n_recommendations, weight_dict={"score":0.1, "popularity":0.1, "members":0.05, "scored_by":0.05, "similarity":0.7}))
    characters_match = get_info_from_code(recommender_algorithms["character_match"](anime_code, n_recommendations))    

    #assing each group of recommendations to its respective row
    recom["similarly_described"] = similar
    recom["hot"] = hot
    recom["beloved"] = beloved
    recom["similar_synopsis"] = similar_synopsis
    recom["genre_match"] = genre_match
    recom["characters_match"] = characters_match
    
    return recom

def get_info_from_code(codes: List[int], input_anime: int = 0):
    recommendations_info = []
    for code in codes:
        try:
            recom_info = anime_info_df.loc[anime_info_df["code"] == code][relevant_fields].to_dict('records')[0]            
            recommendations_info.append(recom_info)
        except:            
            continue

    return recommendations_info

def get_recommendation_weight(input_anime: int, recommended_anime: int):
    try:
        edges = G[input_anime]
    except KeyError:        
        return {"relevance": 0, "text": ""}
    else:
        weight = int(edges.get(recommended_anime, {}).get("weight", 0))
        text = edges.get(recommended_anime, {}).get("text", "")
        return {"relevance":weight, "text": text}

def obtain_random_recommendations(num_recommendations: int) -> Dict:
    recom = defaultdict(list)
    recom["random"] = get_info_from_code(recommender_algorithms["random"](num_recommendations))
    return recom

def get_single_anime_info(anime_code: int):
    try:
        info = anime_info_df.loc[anime_info_df["code"] == anime_code][relevant_fields].to_dict('records')[0]
        return info
    except:
        return {}

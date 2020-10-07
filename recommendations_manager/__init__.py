""" It's in charge of managing communication between the api and the recommerder algoriths """

import os
import pickle
from collections import defaultdict
from typing import List, Dict
from numpy.random import choice
import pandas as pd
from algorithms import *

anime_info_df = pd.read_csv("data/anime_data.csv", encoding="utf-8")

relevant_fields = ['full_title', 'code', 'score', 'image_url', 'synopsis', 'type']

def obtain_recommendations(name: str) -> Dict[str, List[str]]:
    recom = defaultdict(list)    
    #get the codes of the recommendations from the algorithms and then get the info about them
    similar = get_info_from_code(recommender_algorithms["similarity_search"](name.strip()))
    hot = get_info_from_code(recommender_algorithms["soft_clustering"](name.strip()))
    
    #assing each group of recommendations to its respective row
    recom["similarly_described"] = similar
    recom["hot"] = hot

    return recom

def get_info_from_code(codes: List[int]):
    recommendations_info = [anime_info_df.loc[anime_info_df["code"] == code][relevant_fields].to_dict(
        'records')[0] for code in codes]
    return recommendations_info
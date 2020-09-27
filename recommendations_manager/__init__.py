""" It's in charge of managing communication between the api and the recommerder algoriths """

import os
from random import choices
import pickle
from collections import defaultdict
import pandas as pd
from typing import List, Dict
from algorithms import *


anime_info_df = pd.read_csv("data/anime_data.csv", encoding="utf-8")

relevant_fields = ['full_title', 'code', 'score', 'image_url', 'synopsis', 'type']

def obtain_recommendations(names: List[str]) -> Dict[str, List[str]]:    
    recom = defaultdict(list)
    for name in names:        
        try:
            #get the codes of the recommendations from the algorithm
            similarity_recommendations = recommender_algorithms["similarity_search"](
                name.strip())
            clustering_recommendations = recommender_algorithms["soft_clustering"](name.strip())
            recommendation_codes = list(
                set(similarity_recommendations+clustering_recommendations))
            recommendation_codes = choices(recommendation_codes, k=5)
            #use the codes to find the extra information of each anime        
            recommendations_info = [anime_info_df.loc[anime_info_df["code"] == code][relevant_fields].to_dict(
                'records')[0] for code in recommendation_codes]
            recom.update({name: recommendations_info})
            
        except:
            continue 
                    
    return {"recommendations":recom}

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

def obtain_recommendations(names: List[str]) -> Dict[str, List[str]]:    
    recom = defaultdict(list)
    for name in names:        
        try:
            #get the codes of the recommendations from the algorithms
            similarity_recommendations = recommender_algorithms["similarity_search"](
                name.strip())
            clustering_recommendations = recommender_algorithms["soft_clustering"](name.strip())
            print(set(similarity_recommendations+clustering_recommendations))
            recommendation_codes = list(
                set(similarity_recommendations+clustering_recommendations))
            recommendation_codes = choice(recommendation_codes, 5, replace=False)
            #use the codes to find the extra information of each anime        
            recommendations_info = [anime_info_df.loc[anime_info_df["code"] == code][relevant_fields].to_dict(
                'records')[0] for code in recommendation_codes]
            recom.update({name: recommendations_info})
            
        except:
            continue 
                    
    return {"recommendations":recom}

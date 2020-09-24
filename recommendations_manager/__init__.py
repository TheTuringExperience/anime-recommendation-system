""" It's in charge of managing communication between the api and the recommerder algoriths """

import os
import json
import pickle
from collections import defaultdict
import pandas as pd
from typing import List, Dict
from algorithms import *


anime_info_df = pd.read_csv("data/anime_data.csv", encoding="utf-8")

relevant_fields = ['full_title', 'code', 'score', 'image_url', 'synopsis', 'type']

def obtain_recommendations(names: List[str], method: str) -> Dict[str, List[str]]:
    # TODO Scrap the anime data with the code as file name instead of the anime name
    recom = defaultdict(list)
    for name in names:        
        try:
            #get the codes of the recommendations from the algorithm
            recommendation_codes = recommender_algorithms[method](name.strip())  
            #use the codes to find the extra information of each anime
            recommendations_info = [anime_info_df.loc[anime_info_df["code"] == code][relevant_fields].to_dict(
                'records')[0] for code in recommendation_codes]
            recom.update({name: recommendations_info})

        except:
            continue    
        
    return {"recommendations":recom}

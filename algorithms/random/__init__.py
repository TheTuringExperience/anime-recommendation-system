import os
from typing import List

import numpy as np
import pandas as pd

relevent_fields = ["code", "score"]
animes_df = pd.read_csv("./data/anime_data.csv", encoding="utf-8")[relevent_fields]
animes_df = animes_df[animes_df.score>=7.5]

def random_recommender(num_recommendations: int = 5) -> List[int]:
    try:
        recommendations = animes_df.sample(n=num_recommendations, replace=False).code.to_list()        
        return recommendations
    except:
        return []

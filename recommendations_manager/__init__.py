""" It's in charge of managing communication between the api and the recommerder algoriths """

import os
import json
import pickle
from typing import List, Dict
from algorithms import *


with open("data/codes_lookup_table.json", "r") as j:
    codes_lookup_table = json.load(j)
    j.close()

names_lookup_table = {name: code for code, name in codes_lookup_table.items()}

def obtain_recommendations(names: List[str], method: str) -> Dict[str, List[str]]:
    # TODO Scrap the anime data with the code as file name instead of the anime name
    codes = [codes_lookup_table[name] for name in names]
    recom_codes = recommender_algorithms[method](codes)
    recom_names = {names_lookup_table[anime_code]: list(map(lambda x: names_lookup_table[x], recommendations))
                   for anime_code, recommendations in recom_codes.items()}
    return recom_names
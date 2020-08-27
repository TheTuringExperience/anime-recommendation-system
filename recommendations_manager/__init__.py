" It's in charge of managing communication between the api and the recommerder algorith"

from typing import List, Dict
import json
import re
from recommendation_algorithm.recommender import get_neighbours

with open("data/codes_lookup_table.json", "r") as j:
    codes_lookup_table = json.load(j)
    j.close()


def obtain_recommendations(anime_names: List[str]) -> Dict:    
    codes = get_anime_codes([name.lower() for name in anime_names])
    return codes


def get_anime_codes(anime_names: List[str]) -> Dict:
    codes = {name: codes_lookup_table.get(name, None) for name in anime_names}
    return codes

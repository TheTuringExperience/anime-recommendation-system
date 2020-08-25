from typing import List
import json
import re

with open("data/codes_lookup_table.json", "r") as j:
    codes_lookup_table = json.load(j)
    j.close()


def obtain_recommendations(anime_names: List[str]):
    codes = get_anime_codes([name.lower() for name in anime_names])
    return codes


def get_anime_codes(anime_names: List[str]):
    codes = {name: codes_lookup_table.get(name, None) for name in anime_names}
    return codes

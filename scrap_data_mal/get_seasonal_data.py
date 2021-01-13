""" Scrap the data of the anime in a specific season (usually the newest season)"""

import os
import re

from typing import Dict, List

from jikanpy import Jikan
from jikanpy.exceptions import APIException
import pandas as pd

from get_extra_data import * 

jikan = Jikan()

def get_basic_info(year: int, season: str):
    response = jikan.season(year=year, season=season)
    season_anime = response.get("anime")
    seasonal_anime_data = []
    for anime in season_anime:
        if not anime.get("continuing") and anime.get("type") not in ["ONA", 'Special'] \
            and anime.get("score"):
            seasonal_anime_data.append([anime.get("mal_id"), anime.get("url", "").split("/")[-1].lower(), anime.get("score")])            
    return seasonal_anime_data

if __name__ == "__main__":
    year = 2020
    season = "fall"
    basic_info = get_basic_info(year, season)
    animes_info = get_extra_information(basic_info)
    store_info(animes_info)
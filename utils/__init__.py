import re
from typing import List

import pandas as pd

def preprocess_names(anime_names: List) -> List[str]:
    names_lists = [names.split(";;") for names in anime_names]
    #Remove punctuation marks from each name and turn to lowercaps
    names_lists = [list(map(lambda s: re.sub(r'[^\w\s]', '', s.lower()), name_l))
                for name_l in names_lists]
    return names_lists

def preprocess_anime_info(animes_list: List) -> List:    
    search_data = []
    for anime in animes_list:
        titles = anime["show_titles"].split(";;")
        data = {"anime_id":anime["code"], "display_title": titles[0],
                "alternate_titles": list(map(lambda s: s.lower(), titles[1:])),  "type": anime["type"],
                "genres":anime["genres"].split(";"), "release_date":anime["premiered"], "image_url": anime["image_url"]}              
        search_data.append(data)
    return search_data
    

def get_anime_code_from_name(anime_name: str) -> int:
    relevant_fields = ["code", "show_titles"]
    anime_data = pd.read_csv("data/anime_data.csv", encoding="utf-8")[relevant_fields]
    #preprocess the names
    anime_data["name"] = [names_l[0] for names_l in preprocess_names(anime_data["show_titles"].to_list())]
    code = anime_data[anime_data.name == anime_name].code.tolist()[0]

    return code

def get_anime_name_from_code(anime_code: int) -> str:
    relevant_fields = ["code", "show_titles"]
    anime_data = pd.read_csv("data/anime_data.csv", encoding="utf-8")[relevant_fields]
    #preprocess the names
    anime_data["name"] = [names_l[0] for names_l in preprocess_names(anime_data["show_titles"].to_list())]
    name = anime_data[anime_data.code == anime_code].name.tolist()[0]

    return name

def get_genres_list() -> List[str]:
    anime_data_path = "data/anime_data.csv"

    relevant_fields = ["show_titles", "score", "code", "premiered", "genres"]
    animes_df = pd.read_csv(anime_data_path, encoding="utf-8")[relevant_fields]

    #create a list of genres using the "genres" column in the animes_df
    genres = list({genre for genres_list in animes_df.genres.tolist() 
                            for genre in genres_list.split(";")})
    
    return genres

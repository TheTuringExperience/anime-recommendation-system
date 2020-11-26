import re
from typing import List
import pandas as pd

def preprocess_names(anime_names: List) -> List[str]:
    names_lists = [names.split(";;") for names in anime_names]
    #Remove punctuation marks from each name and turn to lowercaps
    names_lists = [list(map(lambda s: re.sub(r'[^\w\s]', '', s.lower()), name_l))
                for name_l in names_lists]
    return names_lists

def get_anime_code_from_name(anime_name: str) -> int:
    relevant_fields = ["code", "show_titles"]
    anime_data = pd.read_csv("data/anime_data.csv", encoding="utf-8")[relevant_fields]
    #preprocess the names
    anime_data["name"] = [names_l[0] for names_l in preprocess_names(anime_data["show_titles"].to_list())]
    code = anime_data[anime_data.name == anime_name].code.tolist()[0]

    return code
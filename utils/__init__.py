import re
from typing import List


def preprocess_names(anime_names: List) -> List[str]:
    names_lists = [names.split(";;") for names in anime_names]
    #Remove punctuation marks from each name and turn to lowercaps
    names_lists = [list(map(lambda s: re.sub(r'[^\w\s]', '', s.lower()), name_l))
                for name_l in names_lists]
    return names_lists
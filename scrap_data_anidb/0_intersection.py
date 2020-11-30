""" Creates a file ./anidb_ids.txt which contains the anidb ids for all the animes in the ../anime_data_anidb.xml file that are also in the
../data/anime_data.csv dile """
from typing import List
import xml.etree.ElementTree as ET

import pandas as pd

df = pd.read_csv("../data/anime_data.csv", encoding="utf-8")
root = ET.parse("../data/anime-titles.xml")

def find_matches():
    names = list(map(lambda s: s.lower(), df.show_titles.to_list()))

    anime_ids = []
    for anime in root.iter("anime"):
        for t in anime.findall("title"):
            if sum([t.text.lower() in name for name in names]):
                anime_ids.append(anime.get("aid"))
                break
    return anime_ids

def save_codes(anime_ids: List):
    with open("./anidb_ids.txt", "w") as f:
        for line in anime_ids:
            f.write(f"{line}\n")
        f.close()

def main():
    anime_ids = find_matches()
    save_codes(anime_ids)

if __name__ == "__main__":
    main()

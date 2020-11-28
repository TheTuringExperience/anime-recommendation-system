import os
import time
import logging
from typing import List

import json
import xml.etree.ElementTree as ET

from requests import get

logging.basicConfig(level=logging.INFO)

time_between_requests = 5
client, clientver = os.getenv("ANIDB_AUTH").split(";")
url = f"http://api.anidb.net:9001/httpapi"
params = {
    "request":"anime",
    "client":client,
    "clientver": clientver,
    "protover":"1"
}

anime_ids = []
with open("./anidb_ids.txt", "r", encoding="utf-8") as f:
    anime_ids = [int(aid) for aid in f.readlines()]
    f.close()

def get_data():
    animes_data = list()
    for idx, aid in zip(range(2), anime_ids):
        params["aid"] = aid
        response = get(url=url, params=params)
        
        # time.sleep(time_between_requests)

        root = ET.fromstring(response.content.decode("utf-8", "replace"))
        
        #extract the data for each relevant field
        genres = list()
        for child in root.iter("tag"):
            if int(child.attrib.get("weight", 0)) > 140:
                genres.append(child.find("name").text)
        genres = list(map(lambda s: s.lower(), genres))

        similar_anime = list()
        for child in root.iter("similaranime"):
            similar_anime.append(child.get("id", ""))

        character_info = list()
        for child in root.iter("character"):
            if child.get("type") == "main character in":
                character_info.append({"id": child.get("id"),
                                    "name": child.findtext("name"),
                                    "description": child.findtext("description")})       
        animes_data.append({"genres": genres, "similar_anime": similar_anime, "characters": character_info})

        logging.info("collected data of: " + str(aid))

    return animes_data


def store_info(animes_data: List):
    filepath = "../data/anime_data_anidb.json"
    # If the file containing the anime data does not exist then create it
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as j:
            json.dump(animes_data, j, ensure_ascii=False)
    # If it exists then just append to it
    else:
        with open(filepath, "r+", encoding="utf-8") as j:
            file_content = json.load(j)
            file_content.extend(animes_data)
            j.seek(0)
            json.dump(file_content, j, ensure_ascii=False)

def main():
    animes_data = get_data()
    store_info(animes_data)

if __name__ == "__main__":
    main()

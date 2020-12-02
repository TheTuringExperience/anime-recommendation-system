""" Scrap from anidb the data for the animes in the ./anidb_ids.txt file and store it in the ../data/anime_data_anidb.json file"""
import os
import time
import logging
from typing import List, Dict

import json
import xml.etree.ElementTree as ET

from requests import get

logging.basicConfig(level=logging.INFO)

time_between_requests = 6
amount_per_session = 250
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

def extract_fields(xml_string: str, default_value: str = "NA") -> Dict:
    try:
        root = ET.fromstring(xml_string.decode("utf-8", "replace"))

        #Extract the data for all the relevant fields
        show_type = root.findtext("type", default_value)
        episode_count = root.findtext("episodecount", default_value)
        start_date = root.findtext("startdate", default_value)
        end_date = root.findtext("enddate", default_value)

        rating = default_value
        if root.find("ratings") is not None:
            # If the rating is aviable then set it
            rating = root.find("ratings").findtext("permanent")

        titles = list()
        for child in root.iter("title"):
            if child.get("type", "") in ["official", "synonym"] and child.get("{http://www.w3.org/XML/1998/namespace}lang", "") in ["en", "x-jat"]:
                titles.append(child.text)

        genres = list()
        for child in root.iter("tag"):
            if int(child.attrib.get("weight", 0)) > 100:
                genres.append(child.findtext("name", default_value))
        genres = list(map(lambda s: s.lower(), genres))

        similar_anime = list()
        for child in root.iter("similaranime"):
            similar_anime.append(child.get("id", default_value))

        character_info = list()
        for child in root.iter("character"):
            if child.get("type") == "main character in":
                character_info.append({"id": child.get("id", default_value),
                                       "name": child.findtext("name", default_value),
                                       "description": child.findtext("description", default_value)})

        data = {"titles": titles, "type": show_type, "episode_count": episode_count,
                "genres": genres, "similar_anime": similar_anime, "start_date": start_date,
                "end_date": end_date, "rating": rating, "characters": character_info}
        return data

    except:
        return dict()


def get_data(start, stop) -> List:
    animes_data = list()
    try: 
        for aid in anime_ids[start: stop]:
            params["aid"] = aid
            response = get(url=url, params=params)

            time.sleep(time_between_requests)
            data = extract_fields(response.content)
            data["aid"] = aid
            animes_data.append(data)

            logging.info("collected data of: " + str(aid))
    except: 
        print('stopped at {}'.format(start))

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
    previous_i = 0
    for i in range(amount_per_session, len(anime_ids), amount_per_session):
        animes_data = get_data(previous_i, i)
        store_info(animes_data)
        print('FINISHED {} - {}. Taking a longer break...'.format(previous_i, i))
        previous_i = i
        time.sleep(300)  # sleep for 300 seconds between sessions
    
    # final time to complete anime_ids
    animes_data = get_data(previous_i, len(anime_ids))
    store_info(animes_data)

if __name__ == "__main__":
    main()

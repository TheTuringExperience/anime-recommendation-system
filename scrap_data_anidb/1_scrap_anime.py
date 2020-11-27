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
    xml_data = list()
    for idx, aid in zip(range(2), anime_ids):
        params["aid"] = aid
        response = get(url=url, params=params)
        
        time.sleep(time_between_requests)        
        xml_data.append(response.content.decode("utf-8", "replace"))
        
    return xml_data


def store_info(xml_data: List):
    filepath = "../data/anime_data_anidb.xml"
    # If the file containing the anime data does not exist then create it
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as x:
            for xml in xml_data:
                x.writelines(xml+"\n")
    # If it exists then just append to it
    else:
        with open("../data/anime_data_anidb.xml", "a", encoding="utf-8") as x:
            for xml in xml_data:
                x.writelines(xml+"\n")

def main():
    xml_data = get_data()
    store_info(xml_data)

if __name__ == "__main__":
    main()

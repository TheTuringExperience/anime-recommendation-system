""" Use Jikanpy to get extra data for the animes in ../data/anime_codes.csv and store it in ../data/anime_data.json"""

import os
import time
import logging
from typing import Dict, List
import json

import pandas as pd

from jikanpy import Jikan
from jikanpy.exceptions import APIException

logging.basicConfig(level=logging.ERROR, filename="scrapping_logs.txt")

jikan = Jikan()

animes_df = pd.read_csv("../data/anime_codes.csv", encoding="utf-8")

def make_request(code: int, sleep_time: int) -> List:
    # wait before making too many requests as per API guidelines
    time.sleep(sleep_time)

    response = jikan.anime(code)
    # remove useless fields
    usless_fields = ["headers", "jikan_url",
                     "request_cache_expiry", "request_cached", "request_hash"]
    for field in usless_fields:
        response.pop(field, None)
    
    #Don't add hentai anime to the data list
    if "Hentai" in response.get("rating", ""):
        return []
    
    return [response]

def get_extra_information(animes_info: List) -> List:
    data = []
    time_between_requests = 3

    for code, name, score in animes_info:        
        try:
            
            data.extend(make_request(code, time_between_requests))

        except APIException as e:
            #If myanimelist refuses the connection stop the scrapping and resume some time later
            logging.error(f"The server did not respond when scrapping {code}: {str(e)}")
            
            try:
                print("Retrying after 15 seconds...")
                data.extend(make_request(code, 15))

            except APIException as e:
                #If myanimelist refuses the connection stop the scrapping and resume some time later
                logging.error(f"The server did not respond again when scrapping {code}: {str(e)}")
                continue 
                
        except Exception as e:
            logging.error(f"Problems getting data for {code}: {str(e)}")
            continue

    return data

def store_info(animes_data: List): 
    filepath = "../data/anime_data.json"
    # If the file containing the anime data does not exist then create it
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as j:            
            json.dump(animes_data, j, ensure_ascii=False)        
    # If it exists then just append to it
    else:
        with open("../data/anime_data.json", "r+", encoding="utf-8") as j:
            file_content = json.load(j)            
            file_content.extend(animes_data)
            j.seek(0)
            json.dump(file_content, j, ensure_ascii=False)

def main():
    animes_data = get_extra_information(animes_df.to_numpy().tolist())
    store_info(animes_data)

if __name__ == "__main__":
    main()
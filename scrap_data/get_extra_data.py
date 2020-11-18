""" Uses Jikanpy to get the image url, decription and some extra info on each of the animes in the anime_data.csv file """

import os
import time
import logging
from typing import Dict, List
import pandas as pd

from jikanpy import Jikan
from jikanpy.exceptions import APIException

logging.basicConfig(level=logging.ERROR, filename="scrapping_logs.txt")

jikan = Jikan()

animes_df = pd.read_csv("../data/anime_codes.csv", encoding="utf-8")

def extract_fields(response: Dict) -> List:
    fields = [response.get("image_url", ""), response.get("synopsis", ""), 
                ";;".join([response.get("title_english", "")] + response.get("title_synonyms", [])),
                response.get("popularity", ""), response.get("members", ""), response.get("scored_by", ""),
                response.get("type", ""), response.get("rating", ""), response.get("premiered", ""),             
                ";".join([studio.get("name", "") for studio in response.get("studios", [])]),
                ";".join([genre.get("name", "").lower() for genre in response.get("genres", [])])
            ]

    return fields

def get_extra_information(animes_info: List) -> List:
    data = []
    time_between_requests = 3

    for code, name, score in animes_info:        
        try:
            response = jikan.anime(code)
            time.sleep(time_between_requests)  # wait before making too many requests as per API guidelines
            
            extra_data = extract_fields(response)
            #Don't add hentai anime to the data list          
            if "Hentai" in extra_data[7]:
                continue
            
            current_row = [code, name, score] + extra_data
            data.append(current_row)           

        except APIException as e:
            #If myanimelist refuses the connection stop the scrapping and resume some time later
            logging.error(f"The server did not respond when scrapping {code}")
            
            try:
                print("Retrying after 15 seconds...")
                time.sleep(15)

                response = jikan.anime(code)
                extra_data = extract_fields(response)                
                #Check that the rating does not contain the word "Hentai"
                if "Hentai" in extra_data[7]:
                    continue

                current_row = row.tolist() + extra_data
                data.append(current_row)

            except APIException as e:
                #If myanimelist refuses the connection stop the scrapping and resume some time later
                logging.error(f"The server did not respond again when scrapping {code}")
                continue 
                
        except Exception as e:
            logging.error(f"Problems getting data for {code}")
            continue

    return data

def store_info(animes_info: List):
    extra_info_df = pd.DataFrame(data=animes_info, columns=["code", "name", "score", "image_url",
                                                            "synopsis", "show_titles", "popularity",
                                                            "members", "scored_by", "type", "rating",
                                                            "premiered", "studios", "genres"])
    extra_info_df.fillna("Not available", inplace=True)
    extra_info_df.to_csv("../data/anime_data.csv", mode="w", index=False)

def main():
    animes_info = get_extra_information(animes_df.to_numpy().tolist())
    store_info(animes_info)

if __name__ == "__main__":
    main()

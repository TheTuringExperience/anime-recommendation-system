""" Uses Jikanpy to get the image url, decription and some extra info on each of the animes in the anime_codes.csv file """

import os
import time
import logging
from typing import Dict, List
import pandas as pd

from jikanpy import Jikan
from jikanpy.exceptions import APIException

jikan = Jikan()

animes_df = pd.read_csv("../data/anime_codes.csv", encoding="utf-8")

def extract_fields(reponse: Dict) -> List:
    fields = [reponse.get("image_url", ""), reponse.get("synopsis", ""), reponse.get("title", ""),
                reponse.get("popularity", ""), reponse.get("members", ""), reponse.get("scored_by", ""),
                reponse.get("type", ""), reponse.get("rating", ""), reponse.get("premiered", ""),             
                ";".join([studio.get("name", "") for studio in reponse.get("studios", [])]),
                ";".join([genre.get("name", "").lower() for genre in reponse.get("genres", [])])
            ]

    return fields

def get_extra_information(animes_info: List) -> List:
    data = []
    time_between_requests = 3

    for code, name, score in animes_info:
        anime_code = code
        try:
            reponse = jikan.anime(anime_code)    
            time.sleep(time_between_requests)  # wait before making too many requests as per API guidelines
            
            current_row = [code, name, score] + extract_fields(reponse)
            data.append(current_row)           

        except APIException as e:
            #If myanimelist refuses the connection stop the scrapping and resume some time later
            logging.error(f"The server did not respond when scrapping {name}: " + str(e))
            
            try:
                print("Retrying after 15 seconds...")
                time.sleep(15)

                anime_info = jikan.anime(anime_code)

                current_row = row.tolist() + extract_fields(reponse)
                data.append(current_row)

            except APIException as e:
                #If myanimelist refuses the connection stop the scrapping and resume some time later
                logging.error(f"The server did not respond again when scrapping {name}: " + str(e))
                continue 
                
        except Exception as e:
            logging.error(f"Problems getting data for {name}: " + str(e))
            continue

    return data

def store_info(animes_info: List):
    extra_info_df = pd.DataFrame(data=animes_info, columns=["code", "name", "score", "image_url",
                                                            "synopsis", "full_title", "popularity",
                                                            "members", "scored_by", "type", "rating",
                                                            "premiered", "studios", "genres"])
    extra_info_df.fillna("Not available", inplace=True)
    extra_info_df.to_csv("../data/new_season.csv", mode="a", index=False)

def main():
    animes_info = get_extra_information(animes_df.to_numpy().tolist())
    store_info(anime_info)

if __name__ == "__main__":
    main()
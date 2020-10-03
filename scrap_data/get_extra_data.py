""" Uses Jikanpy to get the image url, decription and some extra info on each of the animes in the anime_codes.csv file """

import os
import time
import logging
from typing import Dict, List
import pandas as pd
from pprint import pprint
from jikanpy import Jikan
from jikanpy.exceptions import APIException

jikan = Jikan()

animes_df = pd.read_csv("../data/anime_codes.csv", encoding="utf-8")

season_to_month = {"Winter": "01", "Spring": "04", "Summer": "07", "Fall":"10"}

def convert_to_date(anime_season: str):
    if isinstance(anime_season, str):
        season, year = anime_season.split(" ")
        month = season_to_month[season]
        airing_date = "/".join(["01", month, year])
        return airing_date
    return None

def extract_fields(reponse: Dict) -> List:
    fields = [reponse.get("image_url", ""), reponse.get("synopsis", ""), reponse.get("title", ""),
                reponse.get("popularity", ""), reponse.get("members", ""), reponse.get("scored_by", ""),
                reponse.get("type", ""), reponse.get("rating", ""), reponse.get("premiered", ""),             
                ";".join([studio.get("name", "") for studio in reponse.get("studios", [])]),
                ";".join([genre.get(name"name", "").lower() for genre in reponse.get("genres", [])])
            ]

    return fields

def get_extra_information() -> List:
    data = []
    time_between_requests = 3

    for index, row in animes_df.iterrows():
        anime_code = row["code"]
        try:
            reponse = jikan.anime(anime_code)    
            time.sleep(time_between_requests)  # wait before making too many requests as per API guidelines
            
            current_row = row.tolist() + extract_fields(reponse)            
            data.append(current_row)

        except APIException as e:
            #If myanimelist refuses the connection stop the scrapping and resume some time later
            logging.error(f"The server did not respond when scrapping {index}: " + str(e))
            
            try:
                print("Retrying after 15 seconds...")
                time.sleep(15)

                anime_info = jikan.anime(anime_code)

                current_row = row.tolist() + extract_fields(reponse)
                data.append(current_row)

            except APIException as e:
                #If myanimelist refuses the connection stop the scrapping and resume some time later
                logging.error(f"The server did not respond again when scrapping {index}: " + str(e))
                continue 
                
        except Exception as e:
            logging.error(f"Problems getting data for {row['name']}: " + str(e))
            continue

    return data

def main():
    animes_info = get_extra_information()
    extra_info_df = pd.DataFrame(data = animes_info, columns=["code", "name", "score", "image_url", 
                                                                "synopsis", "full_title", "popularity", 
                                                                "members", "scored_by", "type", "rating",
                                                                "premiered", "studios", "genres"])
    extra_info_df["premiered"] = extra_info_df.premiered.apply(convert_to_date)
    extra_info_df.to_csv("../data/anime_data.csv", index=False)

if __name__ == "__main__":
    main()

"""This script takes the ../data/anime_data.json file, extracts the data we need for each anime and saves them in ../data/anime_data.csv """

import os
from typing import List, Dict
import json

import pandas as pd


def extract_fields(anime_dict: Dict) -> List:
    fields = [anime_dict.get("mal_id", ""), anime_dict.get("score", ""), anime_dict.get("image_url", ""),
                anime_dict.get("synopsis", ""), ";;".join([anime_dict.get("title", "")] + anime_dict.get("title_synonyms", [])),
                anime_dict.get("popularity", ""), anime_dict.get("members", ""), anime_dict.get("scored_by", ""),
                anime_dict.get("type", ""), anime_dict.get("rating", ""), anime_dict.get("premiered", ""),
                ";".join([studio.get("name", "") for studio in anime_dict.get("studios", [])]),
                ";".join([genre.get("name", "").lower() for genre in anime_dict.get("genres", [])])
            ]        
    return fields


def convert_json_to_list() -> List:
    animes_data = []
    with open("../data/anime_data.json", "r",encoding="utf-8") as j:
        anime_dicts = json.load(j)
        j.close()

    for anime_dict in anime_dicts:
        animes_data.append(extract_fields(anime_dict))
    
    return animes_data


def store_as_csv(animes_info: List):
    extra_info_df = pd.DataFrame(data=animes_info, columns=["code", "score", "image_url",
                                                            "synopsis", "show_titles", "popularity",
                                                            "members", "scored_by", "type", "rating",
                                                            "premiered", "studios", "genres"])
    extra_info_df.fillna("Not available", inplace=True)
    # Filter out anime that are not TV shows, Movies or ONA
    extra_info_df = extra_info_df[extra_info_df.type.isin(["Movie", "ONA", "TV"])]
    extra_info_df.to_csv("../data/anime_data.csv", mode="w", index=False)


def main():
    animes_list = convert_json_to_list()
    store_as_csv(animes_list)


if __name__ == "__main__":
    main()

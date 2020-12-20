""" Process the data at ../data/anime_planet/anime_data.json and saves it in ../data/anime_planet/process_data.py"""

import os
import json
from typing import List

import pandas as pd


def load_data() -> List:
    with open("../data/anime_planet/anime_data.json", "r") as j:
        data = json.load(j)
        j.close()
    return data


def to_df(anime_data: List):
    df = pd.DataFrame(anime_data)
    #Remove the animes with no tags or ranking
    df.dropna(subset=["tags", "rank"], inplace=True)
    return df


def process_charactes_data(anime_data: List):    
    characters_data = []
    #Turn each character into an entry in the characters_data list
    for anime in anime_data:
        url = anime.get("url", "")
        show_characters = anime.get("characters_data", [])
        for character in show_characters:
            character.update({"anime_url":url})
        characters_data.extend(show_characters)

    df = pd.DataFrame(characters_data)    
    df.dropna(inplace=True)
    df["character_tags"] = df.character_tags.apply(lambda t: ";".join(t))
    df.to_csv("../data/anime_planet/characters_data.csv", encoding="utf-8", index=False)


def process_anime_data(df: pd.DataFrame):    
    #Remove the characters data
    df.drop(["characters_data"], axis=1, inplace=True)
    #Remove \n character from the rank, titles and tags
    df["rank"] = df["rank"].apply(lambda s: str(s).replace("\n", ""))
    df["alt_titles"] = df.alt_titles.apply(lambda s: str(s).replace("\n", ""))
    df["tags"] = df["tags"].apply(lambda x: ";".join(list(map(lambda s: s.replace("\n", ""), x))))
    
    df.to_csv("../data/anime_planet/anime_data.csv", encoding="utf-8", index=False)


def main():
    data = load_data()
    anime_df = to_df(data)    
    process_charactes_data(anime_df[["url", "characters_data"]].to_dict("records"))
    process_anime_data(anime_df)    


if __name__ == "__main__":
    main()

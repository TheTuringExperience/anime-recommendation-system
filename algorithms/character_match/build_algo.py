""" Creates the files needed to run the charecters match recommender algorithm """

from typing import List

import pandas as pd

from sklearn.preprocessing import MultiLabelBinarizer

ap_df = pd.read_csv("../../data/anime_planet/anime_data.csv", encoding="utf-8")
characters_df = pd.read_csv("../../data/anime_planet/characters_data.csv", encoding="utf-8")

#Join characters data with the data of the show they appear in
characters_df = characters_df.join(ap_df.set_index("url"), how="inner", on="anime_url")
#Take only the necessary fields
characters_df = characters_df[["mal_code", "character_tags", "name"]]
#Remove any missing fields
characters_df.dropna(inplace=True)

tags = set([tag.lower() for tags_list in characters_df.character_tags.tolist()
               for tag in tags_list.split(";")])
#Create a categorical representation of the character tags
mlb = MultiLabelBinarizer()
mlb.fit([[tag] for tag in tags])


def get_tags_vector(tags_str: str) -> List:
    tags = tags_str.split(";")
    tags_vector = mlb.transform([[tag.lower()] for tag in tags])[0]
    return tags_vector


def main():    
    characters_df.character_tags = characters_df.character_tags.apply(get_tags_vector)
    characters_df.to_pickle("./characters_df.pkl")


if __name__ == "__main__":
    main()

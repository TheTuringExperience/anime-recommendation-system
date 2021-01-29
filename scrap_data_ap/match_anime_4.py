""" Indentifies the myanimelist code for the anime in ../data/anime_planet/anime_data.csv """

import os
import re
import time

import pandas as pd


def process_mal_names(show_titles: str):
    mal_titles = show_titles.split(";;")
    processed_titles = []
    for title in mal_titles:
        p_title = re.sub(r"[\W]", "-", title.lower().strip())
        p_title = re.sub(r"(--)", "-", p_title)
        p_title = re.sub(r"-$", "", p_title)
        processed_titles.append(p_title)
    #Assing the processed titles to the reference of the mal_data DataFrame    
    return processed_titles


def process_ap_names(titles: pd.DataFrame):
    titles = titles.apply(lambda s: s.split(";;"))
    processed_titles = []
    for title_list in titles:
        p_titles = [re.sub(r"[\W]", "-", title.lower().strip())
                    for title in title_list]
        p_titles = [re.sub(r"(--)", "-", title) for title in p_titles]
        p_titles = [re.sub(r"-$", "", title) for title in p_titles]
        processed_titles.append(p_titles)    
    return processed_titles


def match_names(mal_data: pd.DataFrame, ap_data: pd.DataFrame):
    codes = []
    mal_data.code = mal_data.code.astype(int)
    #TODO: This code is pretty much O(n^3)
    #We iterate over all the anime_planet anime titles
    for p_names in ap_data.processed_names:
        match_found = False
        #We then also iterate over the mal titles
        for idx, row in mal_data.iterrows():     
            #If we find a show two shows that have at least one name in common       
            if any([name in row["processed_names"] for name in p_names]):
                #We append the mal code of that show to alist and break the loop
                codes.append(row["code"])
                match_found = True
                break
        #If the match was not found append a None to keep the list having the same len as the ap_data dataframe
        if not match_found:
            codes.append(None)            

    return codes


def main():
    mal_data = pd.read_csv("../data/anime_data.csv", encoding="utf-8")
    ap_data = pd.read_csv("../data/anime_planet/anime_data.csv", encoding="utf-8")
    #Fill in any empty values
    ap_data.fillna("", inplace=True)
    
    mal_data["processed_names"] = mal_data.show_titles.apply(process_mal_names)
    ap_data["processed_names"] = process_ap_names(ap_data.title + ";;" + ap_data.alt_titles)    
    ap_data["mal_code"] = match_names(mal_data, ap_data)

    #Drop any show with no mal_code
    ap_data.dropna(subset=["mal_code"], inplace=True)

    ap_data.to_csv("../data/anime_planet/anime_data.csv", encoding="utf-8", index=False)


if __name__ == "__main__":
    main()

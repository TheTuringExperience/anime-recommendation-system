""" Uses the links in the ../data/anime_planet directory to scrap the data for each anime and it's main characters
and saves it at ../data/anime_planet/anime_data.json """

import os
import re
import json
import time
import logging

from typing import List, Dict

from requests import get
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, filename="2_logs.txt")

BASE_URL = "https://www.anime-planet.com"
DATA_DIR = "../data/anime_planet"
LINKS_FILE = "anime_links.txt"
DESTINATION_FILE = "anime_data.json"

def get_links() -> List[str]:
    links = []
    with open(os.path.join(DATA_DIR, LINKS_FILE), "r") as f:
        for line in f.readlines():
            links.append(line[:-1])
        f.close()
    #Offset 
    idx = links.index("/anime/is-the-order-a-rabbit-dear-my-sister")
    return links[idx+1:]


def parse_anime_page(anime_url: str) -> Dict:
    #Make the request to get the anime page
    response = get(url=anime_url)

    #Parse the anime page
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", {"itemprop": "name"}).get_text()
    year = soup.find("span", {"class": "iconYear"}).get_text()
    rank = soup.find("div", text=re.compile(r"Rank")).get_text()
    #Some shows don't have alternative titles, but we still might need them when we can find them
    #so try-except block becomes necessary
    alt_titles = ""
    try:
        alt_titles = soup.find("h2", {"class": "aka"}).get_text()
    except:
        pass

    #get the text for each tag of the anime
    tags = [item.get_text() for item in soup.find(
        "div", {"class": "tags"}).find("ul").find_all("li")]
    
    return {"title": title, "year": year, "rank": rank, "alt_titles": alt_titles, "tags": tags}


def parse_character_page(anime_url: str) -> List:
    #Make the request to the characters page
    response = get(url=anime_url+"/characters")

    #Parse the characters page
    soup = BeautifulSoup(response.text, "html.parser")
    characters_data = list()
    #get the table containing the characters data
    table = soup.find("table", {"class": "pure-table"})
    for row in table.find_all("tr"):
        character_info = row.find("td", {"class": "tableCharInfo"})
        url = character_info.a.get("href", "")
        tags = [tag.get_text() for tag in character_info.find_all("li")]

        characters_data.append({"character_url": url, "character_tags": tags})

    return characters_data


def get_anime_data(anime_url: str) -> List:
    url = BASE_URL+anime_url
    name = url.split("/")[-1]

    # Wait some time between requests to avoid getting blocked
    time.sleep(2)

    try:
        anime_data = parse_anime_page(url)
        characters_data = parse_character_page(url)
    except Exception as e:
        logging.error(f" Parsing the data for {name}: {e}")
        return {}
    else:
        logging.info(f" Scrapped the data for: {name}")        
        anime_data["url"], anime_data["characters_data"] = anime_url, characters_data
        return anime_data


def save_data(animes: List):    
    with open(os.path.join(DATA_DIR, "anime_data.json"), "w") as j:
        json.dump(animes, j)
        j.close()
    logging.info(" The data was succesfully saved!")


def main():
    animes = []
    links = get_links()    
    for link in links:
        anime_data = get_anime_data(link)
        animes.append(anime_data)
        
    save_data(animes)

if __name__ == "__main__":
    main()

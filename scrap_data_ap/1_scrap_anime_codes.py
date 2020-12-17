""" Scraps the anime data from https://www.anime-planet.com and stores it in ../data/anime_planet/anime_links.txt"""
import os
import time
import logging

from typing import List

from requests import get
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, filename="1_logs.txt")

URL = "https://www.anime-planet.com/anime/all"
DATA_DIR = "../data/anime_planet"
LINKS_FILE = "anime_links.txt"
TOTAL_PAGES = 262
START_PAGE = 1

def request_page(page_number: int) -> str:

    #Wait some some amount of time between requests so that we don't get blocked
    time.sleep(2)
    #The numbers the include_types key points to are the anime planet codes for TV, Movie and Web anime types
    try:
        response = get(url=URL, params={"include_types": "2,6,5", "page": page_number})
        if response.status_code != 200:
            raise Exception(f" The response code was {response.status_code} instead of 200")

    except Exception as e:
        logging.error(f" Request page #{page_number}: {e}")        
        return ""
    else:
        #If all goes well return the page content
        logging.info(f" Obtained the data for page #{page_number}")
        return response.text

def parse_page(page_content: str) -> List[str]:
    page_links = []
    soup = BeautifulSoup(page_content, "html.parser")    
    try:
        #Parse the page to find the info cards contaning the data
        cards_list = soup.find("ul", {"data-type": "anime"})
        anime_cards = cards_list.find_all("li", {"class": "card"})
    except Exception as e:
        #If there was an error parsing the data return an empty list
        logging.error(f" Error parsing the data for the page: {e}")
        return []
    else:
        #Iterate over the found info cards and extract the link of the anime
        for anime_card in anime_cards:
            link = anime_card.find("a").get("href", "")
            page_links.append(link)
        return page_links

def save_links(links_list):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    
    with open(os.path.join(DATA_DIR, LINKS_FILE), "w") as f:
        #Save the links in a readable format
        f.writelines(f"{link}\n" for link in links_list)
        f.close()

def main():
    links = []    
    for page_number in range(START_PAGE, TOTAL_PAGES+1):
        content = request_page(page_number)
        page_links = parse_page(content)
        links.extend(page_links)        
        
    save_links(links)

if __name__ == "__main__":
    main()

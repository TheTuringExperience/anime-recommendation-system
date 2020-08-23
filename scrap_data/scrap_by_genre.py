""" Obtains the id codes for all the animes listed in myAnimeList and separetes them by genre in .csv files,
but there is overlap due to animes with multiple genres"""

from bs4 import BeautifulSoup
from requests import get
import re
import os
from time import time

genres = []
working_dir = os.getcwd()
genres_directory_path = os.path.join(working_dir, "anime_codes_by_genre")

with open("genres_list.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        genres.append(line.strip().replace(" ", "_"))

for genre_inx in range(1, len(genres)+1):
    page = 0
    anime_data = list()
    start = time()

    while True:
        page += 1
        url = f"https://myanimelist.net/anime/genre/{genre_inx}?page={page}"
        response = get(url=url)
        # since we dont know how many pages there are just keep going until you get a 404 response code
        if response.status_code == 404:
            break
        soup = BeautifulSoup(response.content, "html.parser")
        anime_cards = soup.find_all(
            'div', {'class': re.compile('seasonal-anime js-seasonal-anime')})

        for anime_card in anime_cards:
            # get the id of the anime from its url
            anime_url = anime_card.find(
                'p', class_="title-text").find('a')['href']
            anime_code = re.search(
                "https://myanimelist.net/anime/(\d+)/(.+)", anime_url)

            # get the rating of the anime
            anime_rating = anime_card.find(
                'span', title="Score").text.strip()

            # Making sure that the anime is rated
            if anime_rating.strip() != "N/A":
                anime_data.append(
                    [anime_code.groups()[0], anime_code.groups()[1].lower(), anime_rating])

    # get the name of the genre from the title tag
    genre = soup.find('title').text.split("-")[0].strip()
    file_path = os.path.join(genres_directory_path, genre + ".csv")
    print(f"time spent scrapping {genre} animes: {str(time() - start)}")

    # sort the anime codes list by the rating
    anime_data.sort(key=lambda x: x[2], reverse=True)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("code,name,rating\n")
        for data in anime_data:
            f.write(",".join(data) + "\n")
        f.close()

"""Uses the jikanpy api to scrap the code, name and rating for the animes in each genre in the myanimelist website and stores 
that information in ../data/anime_codes_by_genre/{genre}.csv however there is overlap due to animes with multiple genres"""

import time
from collections import namedtuple
import pandas as pd
from jikanpy import Jikan
from jikanpy.exceptions import APIException

animeEntry = namedtuple("Anime", "code name rating")

jikan = Jikan()
num_genres = 43  # the amount of anime genres in myanimelist.com at the moment
waiting_time = 3  # how long to wait between requests

for genre_id in range(1, num_genres+1):
    page_count = 0
    animes_in_genre = []
    while True:
        try:
            page_count += 1
            time.sleep(waiting_time)
            response = jikan.genre(
                genre_id=genre_id, type="anime", page=page_count)
            animes = response.get("anime")

            for anime in animes:
                code = anime.get("mal_id")
                name = anime.get("url", "").split("/")[-1].lower()
                score = anime.get("score")
                animes_in_genre.append(animeEntry(code, name, score))

        except APIException as e:
            print("There are no more pages for this genre skipping to the next one")
            break

    genre_name = " ".join(response.get("mal_url", {}).get("name").split()[:-1])
    genre_df = pd.DataFrame(data=animes_in_genre)
    genre_df.dropna(inplace=True)
    genre_df.sort_values(by=["rating"], ascending=False, inplace=True)
    genre_df.to_csv(
        f"../data/anime_codes_by_genre/{genre_name}.csv", index=False)
    print(f"Saved the animes in the {genre_name} genre")

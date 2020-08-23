from bs4 import BeautifulSoup
from requests import get
import re

html = get(url="https://myanimelist.net/anime.php")
soup = BeautifulSoup(html.content, "html.parser")
genres_cols = soup.find_all('div', class_='genre-link')[0]
animes_count = []

for genre_col in genres_cols:
    for genre in genre_col:
        genre_count = re.search("\((.+)\)", genre.text)
        for count in genre_count.groups():
            animes_count.append(int("".join(count.split(","))))

print(sum(animes_count))

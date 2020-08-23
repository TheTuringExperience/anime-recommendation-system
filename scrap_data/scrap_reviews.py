from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
import os

working_dir = os.getcwd()
codes_df = pd.read_csv(os.path.join(working_dir, "anime_codes.csv"))

url = "https://myanimelist.net/anime/41353/%20/reviews"
page = get(url=url)
soup = BeautifulSoup(page.content, 'html.parser')
reviews = soup.find_all("div", class_="borderDark")
review_content = reviews[0].find(
    "div", {'class': re.compile("spaceit textReadability word-break")})
print(review_content.text)
print(len(reviews))

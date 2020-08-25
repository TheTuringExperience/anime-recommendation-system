from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
import os

working_dir = os.getcwd()
codes_df = pd.read_csv(os.path.join(working_dir, "anime_codes.csv"))
reviews_list = list()

for index, row in codes_df.iterrows():
    for page_idx in range(5):
        url = f"https://myanimelist.net/anime/{row['code']}/%20/reviews?p={page_idx}"
        page = get(url=url)
        soup = BeautifulSoup(page.content, 'html.parser')
        reviews = soup.find_all("div", class_="borderDark")
        # If there are no reviews in the page break the loop and go to the next anime
        if not reviews:
            break
        for review in reviews:
            review_content = review.find(
                "div", {'class': re.compile("spaceit textReadability word-break")})
            reviews_list.append(review_content)
    print(reviews_list[0])
    print(len(reviews_list))
    exit()

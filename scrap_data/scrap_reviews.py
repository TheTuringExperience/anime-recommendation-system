from bs4 import BeautifulSoup
from requests import get
import re
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.ERROR)

working_dir = os.getcwd()
codes_df = pd.read_csv(os.path.join(working_dir, "anime_codes.csv"))

for index, row in codes_df.iterrows():
    reviews_list = list()
    try:
        for page_idx in range(5):
            url = f"https://myanimelist.net/anime/{row['code']}/%20/reviews?p={page_idx}"
            page = get(url=url)
            soup = BeautifulSoup(page.content, 'html.parser')
            reviews = soup.find_all("div", class_="borderDark")
            # If there are no reviews in the page break the loop and go to the next anime
            if not reviews:
                break

            for review in reviews:
                review_content = review.find("div", {'class': re.compile("spaceit textReadability word-break")})
                reviews_list.append(review_content.text)
    except Exception as e:
        logging.error(
            f"scrapping the reviews for {row['name']} " + str(e))
        continue

    try:
        with open(f"../data/reviews/{row['name']}.txt", "w", encoding="utf-8") as f:
            for review in reviews_list:
                # TODO: find a better way to do this
                cleared_review = re.sub("\s{2}", "", re.sub("(Overall|Story|Animation|Sound|Character|Enjoyment)", "", re.sub("(Helpful)\s*(read more)", "", re.sub(
                    "(\d{1,2}|\d{1,2}/\d{1,2})", "", review))))
                f.writelines(cleared_review)
                f.write("\n")
            f.close()
    except Exception as e:
        logging.error(f"storing the reviews for {row['name']} " + str(e))
        continue

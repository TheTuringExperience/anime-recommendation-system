import os
import re
import time
from random import randint
import logging
import pandas as pd
from jikanpy.exceptions import APIException
from jikanpy import Jikan

logging.basicConfig(level=logging.ERROR)

codes_df = pd.read_csv("../data/anime_codes.csv")
num_reviews = 40
time_between_requests = 2  # in seconds

jikan = Jikan()

#scrap the reviews for the first 1000
for index, row in codes_df[0:1000].iterrows():
    # Put an upper bound on the amoun of reviews to reduce the inbalance problem
    try:
        reviews = jikan.anime(row["code"], extension='reviews')['reviews'][:num_reviews]
        time.sleep(time_between_requests)  # wait before making too many requests as per API guidelines

    
    except APIException as e:
        #If myanimelist refuses the connection stop the scrapping and resume some time later
        logging.error(f"The server did not responded when scrapping {index}: " + str(e))
        break

    except Exception as e:
        logging.error(f"Problems getting data for {row['name']}: " + str(e))

    #if the anime has no reviews then there is no point in making a file for it
    if reviews:
        with open(f"../data/reviews/{row['code']}.txt", "w", encoding="utf-8") as f:
            for review in reviews:                     
                f.writelines(re.sub(r"\s\s+", "", review["content"].replace("\\n", "")))
            f.close()        
    else:
        logging.error(f"No reviews available for {row['name']}")
        continue

    
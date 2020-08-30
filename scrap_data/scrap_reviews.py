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

jikan = Jikan()

for index, row in codes_df[0:500].iterrows():
    # Put an upper bound on the amoun of reviews to reduce the inbalance problem
    try:
        reviews = jikan.anime(row["code"], extension='reviews')['reviews'][:num_reviews]
    
    except APIException as e:
        #If myanimelist refuses the connection stop the scrapping and resume some time later
        logging.error(f"The server did not responded when scrapping {index}")
        break

    except Exception as e:
        print(f"Problems getting data for {row['name']}: " + str(e))

    #if the anime has no reviews then there is no point in making a file for it
    if reviews:
        with open(f"../data/reviews/{row['code']}.txt", "w", encoding="utf-8") as f:
            for review in reviews:                     
                f.writelines(re.sub(r"\s\s+", "", review["content"].replace("\\n", "")))
            f.close()        
    else:
        print(f"No reviews available for {row['name']}")
        continue
    #wait some random time between two and eight seconds scrap the next batch of reviews
    time.sleep(randint(2, 8))

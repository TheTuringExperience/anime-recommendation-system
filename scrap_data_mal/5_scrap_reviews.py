""" Uses Jikanpy to obtain the specified top reviews for the animes stored in the ../data/anime_data.csv file"""

import os
import re
import time

from random import randint
import logging

import pandas as pd
from jikanpy.exceptions import APIException
from jikanpy import Jikan

logging.basicConfig(level=logging.ERROR)

base_dir = "../data/reviews"
source = "../data/anime_data.csv"
codes_df = pd.read_csv(source)
num_reviews = 5
time_between_requests = 4  # in seconds

if not os.path.isdir(base_dir):  # If the base_dir does not exist create it
    os.mkdir(base_dir)

jikan = Jikan()

#scrap the reviews starting from the lower_bound
for index, row in codes_df.iterrows():
    # Put an upper bound on the amoun of reviews to reduce the inbalance problem
    try:
        reviews = jikan.anime(row["code"], extension='reviews')['reviews'][:num_reviews]
        time.sleep(time_between_requests)  # wait before making too many requests as per API guidelines

    except APIException as e:
        #If myanimelist refuses the connection stop the scrapping and resume some time later
        logging.error(f"The server did not respond when scrapping {index}: " + str(e))
        
        try:
            print("Retrying after 15 seconds...")
            time.sleep(15)
            reviews = jikan.anime(row["code"], extension='reviews')['reviews'][:num_reviews]

        except APIException as e:
            #If myanimelist refuses the connection stop the scrapping and resume some time later
            logging.error(f"The server did not respond again when scrapping {index}: " + str(e))
            continue

    except Exception as e:
        logging.error(f"Problems getting data for {row['code']}: " + str(e))
        continue

    #if the anime has no reviews then there is no point in making a file for it
    if reviews:
        line_list = []
        with open(os.path.join(base_dir, f"{row['code']}.txt"), "w", encoding="utf-8") as f:
            for review in reviews:                     
                line_list.append(re.sub(r"\s\s+", " ", review["content"].replace("\\n", " ")) + '\n')
            f.writelines(line_list)
            f.close()        
        print("Collected #{}: {}".format(index, row['code']))

    else:
        logging.error(f"No reviews available for {row['code']}")
        continue

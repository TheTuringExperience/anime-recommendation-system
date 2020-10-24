import os
import re
import time
from argparse import ArgumentParser

from random import randint
import logging

import pandas as pd
from jikanpy.exceptions import APIException
from jikanpy import Jikan

logging.basicConfig(level=logging.ERROR)

parser = ArgumentParser()
parser.add_argument("-s", "--source", help="Source file containing the data of the animes to scrap the reviews of")

args = vars(parser.parse_args())

codes_df = pd.read_csv(f"{args['source']}")
num_reviews = 40
time_between_requests = 3  # in seconds

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
        logging.error(f"Problems getting data for {row['name']}: " + str(e))
        continue


    #if the anime has no reviews then there is no point in making a file for it
    if reviews:
        line_list = []
        with open(f"../data/reviews/{row['code']}.txt", "w", encoding="utf-8") as f:
            for review in reviews:                     
                line_list.append(re.sub(r"\s\s+", " ", review["content"].replace("\\n", " ")) + '\n')
            f.writelines(line_list)
            f.close()        
        print("Collected #{}: {}-{}".format(index, row['code'], row['name']))

    else:
        logging.error(f"No reviews available for {row['name']}")
        continue

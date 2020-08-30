""" Crates a look up table (really just a dictionary) to search an anime's code by it's name"""

import os
import json
import pandas as pd
import re

anime_codes = pd.read_csv("../data/anime_codes.csv", encoding="utf-8")

code_lookup_dict = dict()

for index, row in anime_codes.iterrows():
    code_lookup_dict.update(
        {re.sub("\s\s+", " ", re.sub(r"[-_*]", " ", row["name"])): row["code"]})

with open("../data/codes_lookup_table.json", "w", encoding="utf-8") as j:
    json.dump(code_lookup_dict, j)
    j.close()

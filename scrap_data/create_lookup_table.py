""" Crates a look up table (just a dictionary) to search an anime's code by it's name"""

import os
import json
import pandas as pd

working_dir = os.getcwd()
anime_codes = pd.read_csv(os.path.join(
    working_dir, "anime_codes.csv"), encoding="utf-8")

code_lookup_dict = dict()

for index, row in anime_codes.iterrows():
    code_lookup_dict.update({row["name"]: row["code"]})

with open("../data/code_lookup_table.json", "w", encoding="utf-8") as j:
    json.dump(code_lookup_dict, j)
    j.close()

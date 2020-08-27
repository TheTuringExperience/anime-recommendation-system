""" Uses the nmslib Index to make recommendations """

import os
import pickle
from typing import List
import nmslib

index_dir = "nmslib_index.bin"

index = nmslib.init(method='hnsw', space='cosinesimil')
index.loadIndex(index_dir, load_data=True)

def get_neighbours(codes_list: List[str]):
    pass
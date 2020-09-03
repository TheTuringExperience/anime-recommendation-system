""" Uses the annpy Index to make recommendations """

import os
import pathlib
import pickle
from typing import List, Dict
import numpy as np
from annoy import AnnoyIndex

parent_dir = pathlib.Path(__file__).parent.absolute()

tf_idf_matrix = np.load(os.path.join(parent_dir, "tf_idf_matrix.npy"))
code_to_row = pickle.load(open(os.path.join(parent_dir, "code_to_column.pkl"), "rb"))
row_to_code = {row: code for code, row in code_to_row.items()}

#load the annoy index from disk
index = AnnoyIndex(tf_idf_matrix.shape[1], 'angular')
index.load(os.path.join(parent_dir, 'index.ann'))

def similarity_search(codes: List[str]) -> Dict[int, List[str]]:
    # sets how many recommendations to make per anime
    num_recommendations = 2
    # uses the code of the anime to get it's row in the tf-idf matrix
    recommendations = dict()
    column_idxs = [code_to_row[code] for code in codes]
    for code, idx in codes, column_idxs:
        neighbours = index.get_nns_by_item(idx, num_recommendations)
        neighbours_codes = [row_to_code[neighbour] for neighbour in neighbours]
        recommendations.update({code: neighbours_codes})

    return recommendations

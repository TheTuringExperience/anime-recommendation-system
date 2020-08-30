from annoy import AnnoyIndex
import numpy as np

tf_idf_matrix = np.load("./tf_idf_matrix.npy")

#The number of dimensions is hard-coded, but is should not be
annoyIndex = AnnoyIndex(tf_idf_matrix.shape[1], 'angular') 
annoyIndex.load("./index.ann")

print(annoyIndex.get_nns_by_item(1, 5))

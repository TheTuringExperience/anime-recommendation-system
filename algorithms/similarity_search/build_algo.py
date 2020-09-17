""" Transforms the reviews into a matrix of tf-idf vectors and then creates a new nmslib index, using a HNSW index on Cosine Similarity """

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from annoy import AnnoyIndex
import numpy as np

# After making some analysis I found the most requent words in the reviews corpus and added them to the sklearn stop words list
my_stop_words = text.ENGLISH_STOP_WORDS.union(['like', 'anime', 'one', 'characters', 'really', 'story', 'show', 'character', 'series', 'even',
                                               'first', 'much', 'good', 'also', 'would', 'get', 'well', 'main', 'time', 'still', 'see', 'make', 
                                               'season', 'plot', 'movie', 'pretty', 'episode'])

# TODO: Find a way to not have to hard code the path
reviews_dir = "../../data/reviews"
code_to_row = dict() 
corpus = list()

for index, review_doc in enumerate(os.listdir(reviews_dir)):
    # We use this dictionary later to know the column of each anime in the tf-idf vectors matrix
    code_to_row.update({review_doc[:-4]: index})
    f = open(os.path.join(reviews_dir, review_doc), 'r', encoding="utf-8")
    corpus.append(f.read())
    f.close()

# Create the matrix of tf-idf vectors and converts it to a numpy array
vectorizer = TfidfVectorizer(stop_words=my_stop_words, lowercase=True)
X = vectorizer.fit_transform(corpus).toarray()

annoyIndex = AnnoyIndex(X.shape[1], 'angular')
for i, x in enumerate(X):
    annoyIndex.add_item(i, list(x))

annoyIndex.build(5)  # 5 trees

# Save the code_to_row dict, the matrix of tf_idf vectors and the hsnw index to disk
pickle.dump(code_to_row, open("code_to_row.pkl", "wb"))
np.save("tf_idf_matrix.npy", X)
annoyIndex.save('index.ann')

import re 
import pickle

import numpy as np
import scipy
import scipy.spatial 

import pandas as pd

relevant_fields = ["code", "show_titles"]
anime_data = pd.read_csv("data/anime_data.csv", encoding="utf-8")[relevant_fields]

synopsis_embeddings = np.load(open("algorithms/synopsis_similarity/synopsis_embeddings.npy", "rb"))
anime_codes = pickle.load(open("algorithms/synopsis_similarity/anime_codes.pkl", "rb"))

def synopsis_similarity_recommender(anime_code: int, n_recommendations: int):
    try:        
        query_embedding = synopsis_embeddings[anime_codes.index(anime_code)]
        
        distances = scipy.spatial.distance.cdist([query_embedding], synopsis_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        results = [anime_codes[idx] for idx, _ in results[1:n_recommendations+1]]
        
        return results

    except Exception as e:
        print(e)
        return []

import re 
import pickle

import numpy as np
import scipy
import scipy.spatial 

import pandas as pd

relevant_fields = ["code", "show_titles"]
anime_data = pd.read_csv("data/anime_data_randomanime.csv", encoding="utf-8")[relevant_fields]

synopsis_embeddings = np.load(open("algorithms/synopsis_similarity/synopsis_embeddings_randomanime.npy", "rb"))
anime_codes = pickle.load(open("algorithms/synopsis_similarity/anime_codes_randomanime.pkl", "rb"))


def synopsis_similarity(anime_code: int, n_recommendations: int):
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

def synopsis_similarity_randomanime(anime_code: str, page_number: int, page_size: int = 50):
    def _normalize(val, min_v, max_v):        
            return 1 - (val - min_v)/(max_v - min_v)

    try:

        query_embedding = synopsis_embeddings[anime_codes.index(anime_code)]
        distances = scipy.spatial.distance.cdist([query_embedding], synopsis_embeddings, "cosine")[0]    
        results = zip(range(len(distances)), distances)    
        results = sorted(results, key=lambda x: x[1])
        
        #The first result is always the input anime itself
        min_v = min(results[1:], key=lambda x: x[1])[1]
        max_v = max(results[:], key=lambda x: x[1])[1]
        
        offset = page_size * (page_number - 1)
        result = [(anime_codes[idx], int(_normalize(sim, min_v, max_v) * 100)) 
                for idx, sim in results[offset+1:(page_number*page_size) + 1]]

        codes, similarity_score = list(zip(*result))
        return codes, similarity_score

    except Exception as e:
        print("sinopsis_similarity", e)
        return [], []

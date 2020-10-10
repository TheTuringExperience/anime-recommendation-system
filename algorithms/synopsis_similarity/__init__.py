import re 
import pickle
import numpy as np
import scipy
import scipy.spatial 
import pandas as pd

anime_data = pd.read_csv("data/anime_data.csv", encoding="utf-8")
#preprocess the names
anime_data.name = anime_data.name.apply(lambda x: re.sub(r"\s\s+", " ", re.sub(r"[\_+-]", " ", x)))

synopsis_embeddings = np.load(open("algorithms/synopsis_similarity/synopsis_embeddings.npy", "rb"))
anime_codes = pickle.load(open("algorithms/synopsis_similarity/anime_codes.pkl", "rb"))

def synopsis_similarity_recommender(anime_name: str):
    try:
        code = anime_data[anime_data.name == anime_name].code.tolist()[0]
        query_embedding = synopsis_embeddings[anime_codes.index(code)]
        
        closest_n = 5    
        distances = scipy.spatial.distance.cdist([query_embedding], synopsis_embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        results = [anime_codes[idx] for idx, _ in results[1:closest_n+1]]
        
        return results

    except:        
        return []

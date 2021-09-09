from typing import List
import pickle 
import scipy
import pandas as pd

with open('./algorithms/word2vec/w2v_embeddings_randomanime.data', 'rb') as filehandle:
            # read the data as binary data stream
            embeddings = pickle.load(filehandle)    

animes_df = pd.read_pickle("./algorithms/word2vec/review_df.pkl")

def review_similarity(anime_code: str, n_recommendations: int) -> List[int]:
    try:

        #Reverse mapping of the index
        indices = pd.Series(animes_df.index, index = animes_df['code']).drop_duplicates()# Recommending the Top 5 similar animes
        # drop all duplicate occurrences of the labels 
        indices = indices.groupby(indices.index).first()

        idx = indices[anime_code]
        query_embedding = embeddings[idx]
        
        distances = scipy.spatial.distance.cdist([query_embedding], embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        recommendation = animes_df.iloc[[idx for idx, _ in results[1:n_recommendations] ]].code.tolist()
        
        return recommendation

    except Exception as e:
        print(e)
        return [] 

def review_similarity_randomanime(anime_code: str, page_number: int, page_size: int = 50) -> List[int]:
    def _normalize(val, min_v, max_v):        
            return 1 - (val - min_v)/(max_v - min_v)

    try:

        #Reverse mapping of the index
        indices = pd.Series(animes_df.index, index = animes_df['code']).drop_duplicates()# Recommending the Top 5 similar animes
        # drop all duplicate occurrences of the labels 
        indices = indices.groupby(indices.index).first()

        idx = indices[anime_code]
        query_embedding = embeddings[idx]
        
        distances = scipy.spatial.distance.cdist([query_embedding], embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])

        min_v = min(results[1:], key=lambda x: x[1])[1]
        max_v = max(results[:], key=lambda x: x[1])[1]
        
        offset = page_size * (page_number - 1)
        codes = animes_df.iloc[[idx for idx, _ in results[offset+1:(page_number * page_size) + 1] ]].code.tolist()
        similarity_score = [int(_normalize(sim, min_v, max_v) * 100) for _, sim in results[offset+1:(page_number*page_size) + 1]]

        return codes, similarity_score

    except Exception as e:
        print("review_similarity ", e)
        return [], []

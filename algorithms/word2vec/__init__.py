from typing import List
import pickle 
import scipy
import pandas as pd

with open('./algorithms/word2vec/w2v_embeddings.data', 'rb') as filehandle:
            # read the data as binary data stream
            embeddings = pickle.load(filehandle)    

animes_df = pd.read_pickle("./algorithms/word2vec/review_df.pkl")

def similarity_recommendator(anime_code: str, n_recommendations: int) -> List[str]:
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
        recommendations = animes_df.iloc[[idx for idx, _ in results[1:n_recommendations+1] ]].code.tolist()
        
        return recommendations
    except Exception as e:
        print(e)
        return []

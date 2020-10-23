from typing import List
import pickle 
import scipy
import pandas as pd

with open('./algorithms/word2vec/w2v_embeddings.data', 'rb') as filehandle:
            # read the data as binary data stream
            embeddings = pickle.load(filehandle)    

df = pd.read_pickle("./algorithms/word2vec/review_df.pkl") 

def similarity_recommendator(title: str) -> List[str]:
    try:
        # taking the title and score to store in new data frame called animes
        animes_df = df[['name', 'code']]

        #Reverse mapping of the index
        indices = pd.Series(animes_df.index, index = animes_df['name']).drop_duplicates()# Recommending the Top 5 similar animes
        # drop all duplicate occurrences of the labels 
        indices = indices.groupby(indices.index).first()

        idx = indices[title]
        query_embedding = embeddings[idx]
        
        closest_n = 5    
        distances = scipy.spatial.distance.cdist([query_embedding], embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        recommendations = animes_df.iloc[[idx for idx, _ in results[1:closest_n+1] ]].code.tolist()
        
        return recommendations
    except:
        return []
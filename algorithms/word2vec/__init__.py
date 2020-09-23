from typing import List
import pickle 
import pandas as pd

with open('./algorithms/word2vec/w2v_cosine_sim.data', 'rb') as filehandle:
            # read the data as binary data stream
            cosine_similarities = pickle.load(filehandle)    

df = pd.read_pickle("./algorithms/word2vec/review_df.pkl") 

def similarity_recommendator(title: str) -> List[str]:
    
    # taking the title and rating to store in new data frame called animes
    animes = df[['name', 'rating']]

    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['name']).drop_duplicates()# Recommending the Top 5 similar animes
    # drop all duplicate occurrences of the labels 
    indices = indices.groupby(indices.index).first()

    idx = indices[title]
    sim_scores = sorted(list(enumerate(cosine_similarities[idx])), key = lambda x: x[1], reverse = True)
    sim_scores = [score for score in sim_scores[0:6] if score[0] != idx]
    

    anime_indices = [i[0] for i in sim_scores]
    recommend = animes.iloc[anime_indices]

    return recommend['name'].tolist()        

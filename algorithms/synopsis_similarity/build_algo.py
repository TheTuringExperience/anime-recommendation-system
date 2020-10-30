import re
import time
import pickle
import numpy as np
import scipy
import pandas as pd
from sentence_transformers import SentenceTransformer

#Load the sentence embeddings model
model = SentenceTransformer('bert-base-nli-mean-tokens')

animes_df = pd.read_csv("../../data/anime_data.csv", encoding="utf-8")

def preprocess_data(df):
    #Remove that anoying ending message
    df['synopsis'] = df.synopsis.apply(lambda x: re.sub(r" \[Written by MAL Rewrite\]", "", str(x)))
    #elimnitate any anime with a synopsis that has less than 1 sentence
    df = df[df.synopsis.map(lambda x: len(x.split(". ")) >= 1)]

    #Create a corpus where each synopsis is splitted into a list of sentences
    synopsis_corpus = [synopsis.split(". ") for synopsis in df.synopsis.tolist()]
    codes_list = [code for code in df.code.tolist()]

    return synopsis_corpus, codes_list

def main():
    synopsis_corpus, codes_list = preprocess_data(animes_df)
    corpus_embeddings = []
    for synopsis in synopsis_corpus:
        synopsis_embedding = []
        for sentence in synopsis:
            synopsis_embedding.append(model.encode(sentence))
        #Use the averaged sentence embeddings to represent the content of the synopsis
        corpus_embeddings.append(sum(synopsis_embedding)/len(synopsis_embedding))
    
    #Save the embeddings and the codes list to disk
    np.save(open("./synopsis_embeddings.npy", 'wb'), corpus_embeddings)
    pickle.dump(codes_list, open("./anime_codes.pkl", "wb"))

if __name__ == "__main__":
    main()
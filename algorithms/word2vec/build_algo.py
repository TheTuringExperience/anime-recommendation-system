# Importing necessary libraries
import re
import pickle
import os
import sys

import pandas as pd
import numpy as np
import nltk
import scipy

nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

sys.path.append("../../") #TODO: This is a hack, find a better way

from utils import preprocess_names


def preprocess_data():
    # Reading the data
    relevant_fields = ["code", "show_titles", "score"]
    code_df = pd.read_csv("../../data/anime_data.csv")[relevant_fields]    
    # Read the review data
    reviews_dir = "../../data/reviews"
    all_reviews = list()

    for index, review_doc in enumerate(os.listdir(reviews_dir)):
        current_dict = dict()
            
        # Get the current anime's code
        current_dict['code'] = review_doc.split('.')[0]
        
        # Get the current anime's reviews
        f = open(os.path.join(reviews_dir, review_doc), 'r', encoding="utf-8")
        current_dict['review'] = f.read()
        f.close()
        
        all_reviews.append(current_dict)

    # Create a dataframe of the anime codes and their respective reviews
    review_df = pd.DataFrame(all_reviews)

    # Match the name and score of animes in code_df to the anime reviews dataframe
    review_df['code']=review_df['code'].astype(int)
    df = pd.merge(review_df, code_df, on='code')


    #Utitlity functions for removing ASCII characters, converting lower case, removing stop words, html and punctuation from description
    def _removeNonAscii(s):
        return "".join(i for i in s if  ord(i)<128)

    def make_lower_case(text):
        return text.lower()

    def remove_stop_words(text):
        text = text.split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops]
        text = " ".join(text)
        return text

    def remove_html(text):
        html_pattern = re.compile('<.*?>')
        return html_pattern.sub(r'', text)

    def remove_punctuation(text):
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(text)
        text = " ".join(text)
        return text

    df['cleaned'] = df['review'].apply(_removeNonAscii)
    df['cleaned'] = df.cleaned.apply(func = make_lower_case)
    df['cleaned'] = df.cleaned.apply(func = remove_stop_words)
    df['cleaned'] = df.cleaned.apply(func=remove_punctuation)
    df['cleaned'] = df.cleaned.apply(func=remove_html)
    
    with open("./review_df.pkl", "wb") as filehandle:
        pickle.dump(df[['code']], filehandle)
        filehandle.close()

    return df

def train_word2vec(df: pd.DataFrame, use_saved_file: bool=False):
    if (use_saved_file): 
        with open('w2v_embeddings.data', 'rb') as filehandle:
            # read the data as binary data stream
            embeddings = pickle.load(filehandle)
            return embeddings
    
    #splitting the description into words
    corpus = []
    for words in df['cleaned']:
        corpus.append(words.split())

    # Using the Google pretrained Word2Vec Model 
    # If using for the first time, download and store in ../../data/ 
    # (link: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz)

    EMBEDDING_FILE = '../../data/GoogleNews-vectors-negative300.bin.gz'
    google_word2vec = KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True)

    # Training our corpus with Google Pretrained Model

    google_model = Word2Vec(size = 300, window=5, min_count = 2, workers = -1)
    google_model.build_vocab(corpus)

    #model.intersect_word2vec_format('./word2vec/GoogleNews-vectors-negative300.bin', lockf=1.0, binary=True)

    google_model.intersect_word2vec_format(EMBEDDING_FILE, lockf=1.0, binary=True)

    google_model.train(corpus, total_examples=google_model.corpus_count, epochs = 5)

    # Generate the average word2vec for the each set of anime reviews
    def _vectors(x: pd.DataFrame):
        
        # Creating a list for storing the vectors (description into vectors)        
        array_embeddings = []

        # Reading the each anime review set
        for line in df['cleaned']:
            avgword2vec = None
            count = 0
            for word in line.split():
                if word in google_model.wv.vocab:
                    count += 1
                    if avgword2vec is None:
                        avgword2vec = google_model[word]
                    else:
                        avgword2vec = avgword2vec + google_model[word]
                    
            if avgword2vec is not None:
                avgword2vec = avgword2vec / count
            
                array_embeddings.append(avgword2vec)
        return array_embeddings
    # Calling the function vectors
    embeddings = _vectors(df)

    with open('w2v_embeddings.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(embeddings, filehandle)

    return embeddings


def recommendations(title: str, df: pd.DataFrame, embeddings):
    try:
        # taking the title and score to store in new data frame called animes
        animes_df = df[['code', 'score']]

        #Reverse mapping of the index
        indices = pd.Series(animes_df.index, index = animes_df['code']).drop_duplicates()# Recommending the Top 5 similar animes
        # drop all duplicate occurrences of the labels 
        indices = indices.groupby(indices.index).first()

        idx = indices[title]
        query_embedding = embeddings[idx]
        
        closest_n = 5    
        distances = scipy.spatial.distance.cdist([query_embedding], embeddings, "cosine")[0]

        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        results = animes_df.iloc[[idx for idx, _ in results[1:closest_n+1] ]]
                   
        for index, row in results.iterrows():
            print(f'{row["code"]} score: {row["score"]}')            

    except Exception as e:
        print(f"Error making the recommendation {e}")

def main():
    # if you don't have review_df.pkl, set use_saved_file to False (needed for first time use)
    df = preprocess_data()

    # if you need to retrain or don't have the saved .data file, set use_saved_file to False
    embeddings = train_word2vec(df, use_saved_file=True)

    # if you need to retrain or don't have the saved .data file, set use_saved_file to False
    # tfidf_cosine_similarities = train_tfidf_word2vec(df, use_saved_file=False)

    print("\nRecommendations using word2vec:")
    recommendations(5114, df, embeddings)

if __name__ == "__main__":
    main()

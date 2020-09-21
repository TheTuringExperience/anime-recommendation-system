# Importing necessary libraries
import pandas as pd
import numpy as np
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer

import re
import string
import random
import pickle
import os
import requests
import time
from io import BytesIO

import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from matplotlib import pyplot
from gensim.models import KeyedVectors

def preprocess_data(use_saved_file=False):
    if (use_saved_file): 
        df = pd.read_pickle("./review_df.pkl") 
        return df

    # Reading the data
    code_df = pd.read_csv("../../data/anime_codes.csv")

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

    # Match the name and rating of animes in code_df to the anime reviews dataframe
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
    df.name = df.name.apply(lambda x: re.sub(r"\s\s*", " ", re.sub(r"[\-\_]", " ", x)) )
    df.to_pickle("./review_df.pkl")

    return df

def train_word2vec(df, use_saved_file=False):
    if (use_saved_file): 
        with open('w2v_cosine_sim.data', 'rb') as filehandle:
            # read the data as binary data stream
            cosine_similarities = pickle.load(filehandle)
            return cosine_similarities
    
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
    def vectors(x):
        
        # Creating a list for storing the vectors (description into vectors)
        global array_embeddings
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

    # Calling the function vectors
    vectors(df)

    # finding cosine similarity for the vectors
    cosine_similarities = cosine_similarity(array_embeddings, array_embeddings)

    with open('w2v_cosine_sim.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(cosine_similarities, filehandle)

    return cosine_similarities

def train_tfidf_word2vec(df, verbose=True, use_saved_file=False):
    if (use_saved_file): 
        with open('tfidf_w2v_cosine_sim.data', 'rb') as filehandle:
            # read the data as binary data stream
            cosine_similarities = pickle.load(filehandle)
            return cosine_similarities
    
    #Building TFIDF model and calculate TFIDF score
    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df = 5, stop_words='english')
    tfidf.fit(df['cleaned'])

    # Getting the words from the TF-IDF model
    tfidf_list = dict(zip(tfidf.get_feature_names(), list(tfidf.idf_)))
    tfidf_feature = tfidf.get_feature_names() # tfidf words/col-names
    
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

    # Storing the TFIDF Word2Vec embeddings
    tfidf_vectors = []
    line = 0

    # for each anime's set of reviews
    for desc in corpus: 
        if (verbose): print('loading: {}/{}'.format(line, len(corpus)), end='\r')
        # Word vectors are of zero length (Used 300 dimensions)
        sent_vec = np.zeros(300) 
        # num of words with a valid vector in the anime reviews
        weight_sum =0; 
        # for each word in the anime reviews
        for word in desc: 
            if word in google_model.wv.vocab and word in tfidf_feature:
                vec = google_model.wv[word]
                tf_idf = tfidf_list[word] * (desc.count(word) / len(desc))
                sent_vec += (vec * tf_idf)
                weight_sum += tf_idf
        if weight_sum != 0:
            sent_vec /= weight_sum
        tfidf_vectors.append(sent_vec)
        line += 1
    
    # finding cosine similarity for the vectors
    cosine_similarities = cosine_similarity(tfidf_vectors,  tfidf_vectors)

    # Save file cause it's a really long process to build all the embeddings
    with open('tfidf_w2v_cosine_sim.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(cosine_similarities, filehandle)
    
    return cosine_similarities

def recommendations(title, df, cosine_similarities):
    
    # taking the title and rating to store in new data frame called animes
    animes = df[['name', 'rating']]

    #Reverse mapping of the index
    indices = pd.Series(df.index, index = df['name']).drop_duplicates()# Recommending the Top 5 similar animes
    # drop all duplicate occurrences of the labels 
    indices = indices.groupby(indices.index).first()

    idx = indices[title]
    sim_scores = sorted(list(enumerate(cosine_similarities[idx])), key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]
    anime_indices = [i[0] for i in sim_scores]
    recommend = animes.iloc[anime_indices]
    
    count = 0
    for index, row in recommend.iterrows():
        print('{}. {}, similarity: {}, rating: {}'.format(count+1, row['name'], sim_scores[count][1], row['rating']))
        count += 1

def main():
    # if you don't have review_df.pkl, set use_saved_file to False (needed for first time use)
    df = preprocess_data(use_saved_file=True)

    # if you need to retrain or don't have the saved .data file, set use_saved_file to False
    cosine_similarities = train_word2vec(df, use_saved_file=True)

    # if you need to retrain or don't have the saved .data file, set use_saved_file to False
    # tfidf_cosine_similarities = train_tfidf_word2vec(df, use_saved_file=False)

    print("\nRecommendations using tfidf word2vec:")
    recommendations('cowboy bebop', df, tfidf_cosine_similarities)

if __name__ == "__main__":
    main()
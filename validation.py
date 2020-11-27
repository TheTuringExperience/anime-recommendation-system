from sklearn.metrics import ndcg_score
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import os
import sys

from algorithms.word2vec import similarity_recommendator
from algorithms.soft_clustering import soft_clustering_recommendator
from algorithms.synopsis_similarity import synopsis_similarity_recommender
from recommendations_manager import obtain_recommendations, obtain_random_recommendations
from utils import preprocess_names, get_anime_code_from_name

def print_matches(recs, data):
    for key in recs:
        print('\nrow: {}'.format(key))
        current_row = recs[key]
        true_rel_array = []
        curr_score_array = []
        for item in current_row:
            curr_code = item['code']
            if (curr_code in data.mal_id.values):
                match = data.loc[data['mal_id'] == curr_code].iloc[0]
                print("item: {}, match_name: {}, rec_count: {}".format(curr_code, match['name'], match['relevance']))
                curr_score_array.append(1)
                true_rel_array.append(1)
            else:
                curr_score_array.append(1)
                true_rel_array.append(0)

        ndcg_value = ndcg_score(np.asarray([true_rel_array]), np.asarray([curr_score_array]))
        print("ndcg: {}".format(ndcg_value))

# Input: recommendations from recommendation manager 
# Output: dictionary with each row key and ndcg score
# TODO: Use similarity score (cosine sim value or otherwise) to compare to normalized relevancy for better accuracy
# currently just uses a 1 or 0 in the arrays
def score_with_ndcg(recs, data):
    score_dict = {}
    for key in recs:
        current_row = recs[key]
        true_rel_array = []
        curr_score_array = []
        for item in current_row:
            curr_code = item['code']
            if (curr_code in data.mal_id.values):
                # match = data.loc[data['mal_id'] == curr_code].iloc[0]
                curr_score_array.append(1)
                true_rel_array.append(1)
            else:
                curr_score_array.append(1)
                true_rel_array.append(0)

        if (len(true_rel_array) > 0):
            ndcg_value = ndcg_score(np.asarray([true_rel_array]), np.asarray([curr_score_array]))
            score_dict[key] = ndcg_value
    
    return score_dict

# Input: name of anime, boolean if printing is wanted
# Output: ncdg scores
def get_scores(anime_name, verbose=False):
    recs = obtain_recommendations(anime_name)
    anime_code = get_anime_code_from_name(anime_name)
    if verbose: print("current anime code: {}, name: {}".format(anime_code, anime_name))

    try:
        data = pd.read_csv('data/recommendations/{}.txt'.format(anime_code), sep=",", header=None)
        data.columns = ["mal_id", "relevance", "name"]
    except FileNotFoundError:
        if verbose: print('no recommendations found for {}'.format(anime_code))
        return {}
    except:
        if verbose: print('error reading file for {}'.format(anime_code))
        return {}

    if verbose: print_matches(recs, data)
    
    return score_with_ndcg(recs, data)

# Input: name of anime and array of recommended anime codes for that anime
# Output: ndcg score
def score_individual_rec(anime_name, rec_array):
    anime_code = get_anime_code_from_name(anime_name)
    try:
        data = pd.read_csv('data/recommendations/{}.txt'.format(anime_code), sep=",", header=None)
        data.columns = ["mal_id", "relevance", "name"]
    except FileNotFoundError:
        print('no recommendations found for {}'.format(anime_code))
        return {}

    true_rel_array = []
    curr_score_array = []
    for curr_code in rec_array:
        if (curr_code in data.mal_id.values):
            # match = data.loc[data['mal_id'] == curr_code].iloc[0]
            curr_score_array.append(1)
            true_rel_array.append(1)
        else:
            curr_score_array.append(1)
            true_rel_array.append(0)

    ndcg_value = ndcg_score(np.asarray([true_rel_array]), np.asarray([curr_score_array]))

    return ndcg_value

# Validation with a large amount of random anime
# Output: average ndcg scores of each key in dictionary
def random_scoring(random_state=42, test_size=0.3):
    anime_names = pd.read_csv("data/anime_data.csv")["show_titles"].tolist()
    names_lists = preprocess_names(anime_names)
    x_train, x_test = train_test_split(names_lists, test_size=test_size, random_state=random_state)
    # print(x_test)

    full_dict = {}
    sample_recs = obtain_recommendations(x_test[0][0])
    for key in sample_recs:
        full_dict[key] = 0

    error_count = 0
    for item_list in x_test:
        item = item_list[0]
        curr_dict = get_scores(item)
        if (not bool(curr_dict)): error_count += 1
        for key in curr_dict:
            full_dict[key] += curr_dict[key]
    
    test_set_length = len(x_test) - error_count
    for key in full_dict:
        full_dict[key] = full_dict[key] / test_set_length
    
    return full_dict

# TODO: create a mock algorithm that just takes cosine sim between vectors of genre or something

def main():
    score_dict = get_scores('cowboy bebop', verbose=False)
    print(score_dict)

    test_array = similarity_recommendator('cowboy bebop')
    score = score_individual_rec('cowboy bebop', test_array)
    print(score)

    test_array = soft_clustering_recommendator('cowboy bebop', 'score')
    score = score_individual_rec('cowboy bebop', test_array)
    print(score)

    test_array = synopsis_similarity_recommender('cowboy bebop')
    score = score_individual_rec('cowboy bebop', test_array)
    print(score)

    average_ncdg = random_scoring(test_size=0.01)
    print(average_ncdg)

if __name__ == "__main__":
    main()
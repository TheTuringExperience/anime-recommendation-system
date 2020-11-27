from sklearn.metrics import ndcg_score
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import os
import sys

from algorithms.word2vec import similarity_recommendator
from algorithms.soft_clustering import soft_clustering_recommendator
from algorithms.genre_match import genre_match_recommender
from algorithms.synopsis_similarity import synopsis_similarity_recommender

from recommendations_manager import obtain_recommendations, obtain_random_recommendations
from utils import preprocess_names, get_anime_code_from_name, get_anime_name_from_code, get_genres_list

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
# TODO: allow selection of individual algorithm
def score_individual_rec(anime_name, rec_array, verbose=False):
    anime_code = get_anime_code_from_name(anime_name)
    try:
        data = pd.read_csv('data/recommendations/{}.txt'.format(anime_code), sep=",", header=None)
        data.columns = ["mal_id", "relevance", "name"]
    except FileNotFoundError:
        if verbose: print('no recommendations found for {}'.format(anime_code))
        return -1
    except:
        if verbose: print('error reading file for {}'.format(anime_code))
        return -1

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

# Validation with a large amount of random anime for specific algorithm
# Output: average ndcg scores of specific algorithm
# TODO: allow selection of individual algorithm
def random_individual_scoring(random_state=42, test_size=0.3):
    anime_names = pd.read_csv("data/anime_data.csv")["show_titles"].tolist()
    names_lists = preprocess_names(anime_names)
    x_train, x_test = train_test_split(names_lists, test_size=test_size, random_state=random_state)

    error_count = 0
    total_score = 0
    for item_list in x_test:
        item = item_list[0]
        test_array = soft_clustering_recommendator(item, 'score')
        # test_array = genre_match_recommender(item)
        score = score_individual_rec(item, test_array)
        if(score == -1): error_count += 1
        else: total_score += score
    
    test_set_length = len(x_test) - error_count
    avg_score = total_score / test_set_length
    
    return avg_score


def main():
    score_dict = get_scores('cowboy bebop', verbose=False)
    print(score_dict)

    # test_array = similarity_recommendator('cowboy bebop')
    # score = score_individual_rec('cowboy bebop', test_array)
    # print(score)

    # test_array = soft_clustering_recommendator('cowboy bebop', 'score')
    # score = score_individual_rec('cowboy bebop', test_array)
    # print(score)

    # test_array = synopsis_similarity_recommender('cowboy bebop')
    # score = score_individual_rec('cowboy bebop', test_array)
    # print(score)

    genre_list = get_genres_list()

    # for i in range(10):
    # test_array = genre_match_recommender(get_anime_name_from_code(5114), genre_list[:i])
    test_array = genre_match_recommender(get_anime_name_from_code(5114), [genre_list[0]])
    score = score_individual_rec(get_anime_name_from_code(5114), test_array)
    print(score)

    for item in test_array:
        print(get_anime_name_from_code(item))

    # average_ndcg = random_scoring(test_size=0.01)
    # print(average_ndcg)

    # avg_indv_ndcg = random_individual_scoring(test_size=0.01)
    # print(avg_indv_ndcg)

if __name__ == "__main__":
    main()
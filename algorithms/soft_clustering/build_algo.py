""" Creates the files needed to run the soft_culstering recommender system """

import os
import re
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

files_path = "../../data/anime_codes_by_genre/"
#list all the .csv in that path
anime_files = os.listdir(files_path)

#create a list of the available genres
anime_genres = [file.lower().split(".")[0] for file in anime_files]

#create a one_hot encoded representation of the genres
one_hot = OneHotEncoder(handle_unknown="ignore")
one_hot.fit([[genre] for genre in anime_genres])

def main():
    #create a dict where the key is the anime name and the value is a one_hot representation of it's genres
    global animes_with_genres, name_to_code
    animes_with_genres = dict()
    name_to_code = dict()
    for file_name in anime_files:
        #load the csv of the file and filter out the animes with and score lower than 6.5
        current_df = pd.read_csv(os.path.join(files_path, file_name), encoding="utf-8")
        current_df = current_df[current_df.rating >= 6.5]   
        for name, code in current_df[["name", "code"]].values.tolist():
            cleaned_name = re.sub(r"\s\s+", " ", re.sub(r"[\_+-]", " ", name))
            name_to_code.update({cleaned_name: code})
            #each time you find the name of an anime in the csv for a genre add the one_hot representation \
            # of the genre to the existing vector for that anime
            animes_with_genres.setdefault(code, np.zeros((1,len(anime_files))))
            genre = file_name.lower().split(".")[0]
            animes_with_genres[code] += one_hot.transform([[genre]]).toarray()    

if __name__ == "__main__":
    main()
    #save the dict as a binary pickle file
    pickle.dump(animes_with_genres, open("./anime_genres.pickle", "wb"))
    pickle.dump(name_to_code, open("./name_to_code.pickle", "wb"))

# Anime Recommendation System

### Motivation:
------
We love anime, some of our favorite stories, characters and worlds come from anime. However, there is a problem with the current state of the medium.

There is so much new anime coming out each season that whatever is the most popular at the moment completely dominates the conversation in the community and as a result a lot of older and incredible, anime is forgotten, even if they came out just a couple of months ago.

This system uses deep learning algorithms, along side other techniques, to give people qualitative recommendations based on shows they previously enjoyed, without putting much weight into how recent the recommended shows are. This way people get good recommendations and there is also a better chance for older anime to shine.

### Here is a summary of how each recommender algorithm works:
------
* **Review Similarity:** This system takes the top reviews of an anime and uses the [Skip-Gram](https://arxiv.org/abs/1301.3781") model implemented in the [Gensim](https://radimrehurek.com/gensim/) library to create vector representations of all the words in the review, then it averages them to create a single vector representation of the reviews of the anime. To make a recommendation, we take the review embedding of an anime and use the [cosine distance](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html?highlight=cdist#scipy.spatial.distance.cdist) metric to find it's closest neighbours which are returned as the recommendations.

* **Synopsis Similarity:** We take the synopsis of an anime and use the bert-base-nli-mean-tokens model from the [SentenceTransformers](https://github.com/UKPLab/sentence-transformers) library to create a sentence embedding for the synopsis of the anime. To make a recommendation, we take the synopsis embedding and use the [cosine distance](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html?highlight=cdist#scipy.spatial.distance.cdist) metric to find it's closest neighbours which are returned as the recommendations.

* **Soft Clustering:** This system returns the highest rated animes with the most amount of genres in common with the inserted anime as recommendations. It can also return the most recent animes with the most amount of genres in common with the inserted anime (We did some alpha testing and people requested this last feature to be added </3)

* **Character Similarity:** This systems uses the very detailed character tags from [Anime-Planet](https://www.anime-planet.com/characters/) to make recommendations. It uses the tags of an anime's main character and finds similar characters in other shows which it returns as the recommenedations.

* **Validation:** This isn't a recommender algorithm but it's the one we'll use to determine the quality of recommendations churned out by the above algorithsm. It uses the NDCG metrics for scoring the relevance and the order of the suggested algorithms. The true relevance scores are currently determined by crowd sourced recommendations in MAL. The validation pipeline will also be used to measure prediction accuracy for hyperparameter tuning (for example, we could test with logistic regression on tag vectors, genre vectors, release date, director, etc. and tune hyperparameters to find most suitable set). Keep in mind when comparing completely different rows that seasonality or popularity plays a big deal in the score (new or less known animes don't have as much say in recs). Hence, it shouldn't be used to judge items all too harshly; we might even consider training models to find out what makes these recommendations work and use those as metrics in the future.

### Usage:
------
NOTE: you can skip the first 2 steps if you just download the prebuilt models here: https://drive.google.com/drive/folders/1s9lUnI_4QSF-VKPGQiciFXiTrkD48ois?usp=sharing

1. First you'd need to scrape the data using the python scripts (ordered 1-5) in the ./scrap_data folder
    - `cd scrap_data`
    - `python scrap_by_genre_1.py`
2. Then you'll have to build the algorithms from the data scraped, you can do this by running the individual build_algo.py files in each algorithms/*/. folder. For examples:
    - `cd algorithms`
    - `cd word2vec`
    - `python build_algo.py`
3. Finally, once you have the files you need, you can run the following to set up the API and see it running on port localhost:8000
    - `uvicorn main:api --reload`


You can find the repo for the UI [here](https://github.com/chriskok/AnimeRec)
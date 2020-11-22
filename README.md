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

### Usage:
------
NOTE: you can skip the first 2 steps if you just download the prebuilt models here: ~GOOGLE DRIVE LINK TBD~

1. First you'd need to scrape the data using the python scripts (ordered 1-5) in the ./scrap_data folder
    - `cd scrap_data`
    - `python 1_scrap_by_genre.py`
2. Then you'll have to build the algorithms from the data scraped, you can do this by running the individual build_algo.py files in each algorithms/*/. folder. For examples:
    - `cd algorithms`
    - `cd word2vec`
    - `python build_algo.py`
3. Finally, once you have the files you need, you can run the following to set up the API and see it running on port localhost:5000
    - `uvicorn main:api --reload`

You can check out the system in action [here](http://3.131.210.47:5000/)

You can also find the repo for the UI [here](https://github.com/chriskok/AnimeRec)



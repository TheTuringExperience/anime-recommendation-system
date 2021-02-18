""" Creates and stores a weighted graph in which the nodes are animes and the edges signify user recommendations
the weight of an each is the number of people how though the recommendation was usefull """
import pandas as pd
import networkx as nx
import gc

user_recoms_df = pd.read_csv("../data/recommendations.csv", encoding="utf-8")
output_df = pd.read_pickle("../algorithms/genre_match/full_df.pkl")

def calculate_ranking_score(row, config_dict):
    score = row['score'] * config_dict['score']
    popularity = row['popularity'] * config_dict['popularity']
    members = row['members'] * config_dict['members']
    scored_by = row['scored_by'] * config_dict['scored_by']
    similarity = row['similarity'] * config_dict['similarity']
    return score + popularity + members + scored_by + similarity

def get_ranking_scores(anime_code):
    try:
        df = output_df.copy()
        weight_dict={"score":0.1, "popularity":0.1, "members":0.05, "scored_by":0.05, "similarity":0.7}
        df["similarity"] = df[anime_code]
        df['ranking_score'] = df.apply(calculate_ranking_score, axis=1, args=(weight_dict,))

        ranking_dict = df.ranking_score.to_dict()
        ranking_dict.pop(anime_code) 
        return ranking_dict
    except KeyError:
        return {}

def print_edge(G, input_code, rec_code):
    try:
        edges = G[input_code]
    except KeyError:        
        return {"relevance": 0, "text": "", "ranking_score": 0.0}
    else:
        weight = int(edges.get(rec_code, {}).get("weight", 0))
        text = edges.get(rec_code, {}).get("text", "")
        ranking_score = float(edges.get(rec_code, {}).get("ranking_score", 0.0))
        print(f"relevance: {weight}, text: {text}, ranking_score: {ranking_score}")

def create_nodes(G: nx.Graph):
    # all_animes = set(user_recoms_df.mal_id_0.to_list() + user_recoms_df.mal_id_0.to_list())
    all_animes = output_df.index.to_list()
    for node in all_animes:
        G.add_node(node)

def create_edges(G: nx.Graph):
    # for idx, row in user_recoms_df.iterrows():
    #     G.add_edge(row["mal_id_0"], row["mal_id_1"], weight=row["relevance"], text=row["text"])
    
    all_animes = output_df.index.to_list()
    count = 0

    for anime_code_1 in all_animes:
        ranking_dict = get_ranking_scores(anime_code_1)
        for anime_code_2 in all_animes:
            if (anime_code_1 == anime_code_2): continue
            mal_id_1 = anime_code_1 if anime_code_1 < anime_code_2 else anime_code_2
            mal_id_0 = anime_code_1 if anime_code_1 > anime_code_2 else anime_code_2
            user_recom = user_recoms_df[(user_recoms_df['mal_id_0'] == mal_id_0) & (user_recoms_df['mal_id_1'] == mal_id_1) ]

            if (user_recom.shape[0] > 0): 
                curr_recom = user_recom.iloc[0]
                G.add_edge(anime_code_1, anime_code_2, weight=curr_recom["relevance"], text=curr_recom["text"], ranking_score=ranking_dict[anime_code_2])
            else:
                G.add_edge(anime_code_1, anime_code_2, weight=0, text="", ranking_score=ranking_dict[anime_code_2])
        count += 1
        if (count % 100 == 0): print('Added {} of {} anime to graph'.format(count, len(all_animes)))

def main():
    graph = nx.Graph()
    create_nodes(graph)
    create_edges(graph)
    nx.readwrite.gpickle.write_gpickle(graph, "./graph.pkl")

if __name__ == "__main__":
    main()

    # # Testing the constructed graph
    # G = nx.readwrite.gpickle.read_gpickle("./graph.pkl")
    # print_edge(G, 10620, 1535)
    # print_edge(G, 1535, 23283)
    # print_edge(G, 1535, 1)
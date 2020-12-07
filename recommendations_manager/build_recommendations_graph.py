""" Creates and stores a weighted graph in which the nodes are animes and the edges signify user recommendations
the weight of an each is the number of people how though the recommendation was usefull """
import pandas as pd
import networkx as nx

user_recoms_df = pd.read_csv("../data/recommendations.csv", encoding="utf-8")

def create_nodes(G: nx.Graph):
    all_animes = set(user_recoms_df.mal_id_0.to_list() + user_recoms_df.mal_id_0.to_list())
    for node in all_animes:
        G.add_node(node)

def create_edges(G: nx.Graph):
    for idx, row in user_recoms_df.iterrows():
        G.add_edge(row["mal_id_0"], row["mal_id_1"], weight=row["relevance"], text=row["text"])

def main():
    graph = nx.Graph()
    create_nodes(graph)
    create_edges(graph)
    nx.readwrite.gpickle.write_gpickle(graph, "./graph.pkl")

if __name__ == "__main__":
    main()

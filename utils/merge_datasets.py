import pandas as pd

df = pd.read_csv("../data/anime_data.csv", encoding="utf-8")
df_randomanime = pd.read_json("../data/randomanime-anime-list.json", encoding="utf-8")

indexes = df_randomanime["my_anime_list_id"].tolist()
df.set_index("code", inplace=True, drop=False)
df = df.reindex(indexes)

df.dropna(inplace=True)
df.to_csv("../data/anime_data_randomanime.csv", encoding="utf-8", index=False)
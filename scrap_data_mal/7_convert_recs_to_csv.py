from os import listdir
from os.path import isfile, join
import pandas as pd

rec_folder_path = "../data/recommendations"
recfiles = [f for f in listdir(rec_folder_path) if isfile(join(rec_folder_path, f))]

filename = recfiles[0]
filecode = int(filename.split('.')[0])

full_df = pd.read_csv('{}/{}'.format(rec_folder_path, filename), sep=",", header=None, usecols=range(2))
full_df.columns = ["mal_id", "relevance"]
full_df['query_id'] = [filecode for i in range(full_df.shape[0])]

for filename in recfiles[1:]:
    filecode = int(filename.split('.')[0])

    data = pd.read_csv('{}/{}'.format(rec_folder_path, filename), sep=",", header=None, usecols=range(2))
    data.columns = ["mal_id", "relevance"]
    data['query_id'] = [filecode for i in range(data.shape[0])]
    full_df = full_df.append(data, ignore_index=True)

full_df["max"] = full_df[["mal_id", "query_id"]].max(axis=1)
full_df["min"] = full_df[["mal_id", "query_id"]].min(axis=1)
full_df = full_df.sort_values('query_id', ascending=True).drop_duplicates(subset=['max', 'min'])
full_df = full_df.drop(['query_id', 'mal_id'], axis=1)
full_df = full_df.rename(columns={"max": "mal_id_0", "min": "mal_id_1"})
full_df.to_csv('../data/recommendations.csv', index=False, header=True)
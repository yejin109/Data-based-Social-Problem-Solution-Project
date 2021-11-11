import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

import config
from utils.analytics import key_search, scoring, get_similar_clusters

# config
model_embedding = Word2Vec.load('result/w2v_model.model')
embeddings = model_embedding.wv.vectors

token = np.array(model_embedding.wv.index_to_key)
token_info = pd.read_csv('result/token_info.csv', index_col=0)

token2cluster = {}
for row in range(token_info.shape[0]):
    each = token_info.iloc[row]
    token2cluster[each[0]] = each[1]
model_clustering = token_info['Cluster']
cluster_types = np.unique(model_clustering)

cluster2token = {}

for i in cluster_types:
    cluster2token[i] = token[model_clustering == i]

########################################################################################################################
# 유사한 cluster로 keyword 특징 찾기
########################################################################################################################
similarity = cosine_similarity(embeddings)

for i in range(similarity.shape[0]):
    similarity[i, i] = 0

key = '페미'
search_keys = config.search_keys
overall_results = get_similar_clusters(token, similarity, cluster2token, token2cluster, key)

for search_key in search_keys:
    result = get_similar_clusters(token, similarity, cluster2token, token2cluster, search_key)
    overall_results = pd.concat((overall_results, result), axis=0)

# overall_results.to_csv('result/search_key_result.csv')

print()

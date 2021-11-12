import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

from yonsei_social import config
from yonsei_social.utils.analytics import key_search, scoring, get_similar_clusters

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
# similarity = cosine_similarity(embeddings)
#
# for i in range(similarity.shape[0]):
#     similarity[i, i] = 0
#
# search_keys = config.search_keys
# overall_results = get_similar_clusters(token, similarity, cluster2token, token2cluster, search_keys[0])
#
# for search_key in search_keys[1:]:
#     if search_key not in token:
#         continue
#     result = get_similar_clusters(token, similarity, cluster2token, token2cluster, search_key)
#     overall_results = pd.concat((overall_results, result), axis=0)
#
# politic_keys = config.politic_keys
# for politic_key in politic_keys:
#     if politic_key not in token:
#         continue
#     result = get_similar_clusters(token, similarity, cluster2token, token2cluster, politic_key)
#     overall_results = pd.concat((overall_results, result), axis=0)
# overall_results.to_csv('result/key_result.csv')

########################################################################################################################
# 유사한 cluster로 keyword 특징 찾기
########################################################################################################################
results = pd.read_csv('result/key_result.csv', index_col=0)
clusters = list(results.columns)[:len(list(results.columns))]
results_cluster = results.loc[:, clusters]
results.loc[:, clusters] = (results_cluster-results_cluster.mean())/results_cluster.std()
results.fillna(0, inplace=True)
print()

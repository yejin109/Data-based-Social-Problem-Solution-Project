import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

import config
from utils.analytics import key_search, scoring

# config
gmm_components = config.gmm_components

model_embedding = Word2Vec.load('result/total/w2v_model.model')
embeddings = np.loadtxt('result/total/embeddings.txt')

model_clustering = np.loadtxt('result/total/clustered.txt')
voca = np.array(model_embedding.wv.index_to_key)
cluster_types = np.unique(model_clustering)

voca_clusters = {}

for i in range(gmm_components):
    voca_clusters[i] = voca[model_clustering == i]

########################################################################################################################
# 유사한 cluster로 keyword 특징 찾기
########################################################################################################################
similarity = cosine_similarity(embeddings)

for i in range(similarity.shape[0]):
    similarity[i, i] = 0

key = '페미'
key_idx = np.argwhere(voca == key)[0][0]

pairwise_distance = similarity[key_idx, :]

top_1000_idx = np.argsort(pairwise_distance)[::-1][:1000]
top_1000_vocas = voca[top_1000_idx]

result = {}
for voca_cluster_idx in list(voca_clusters.keys()):
    result[voca_cluster_idx] = 0

for top_1000_voca in top_1000_vocas:
    each_cluster = voca_dictionary[top_1000_voca]
    result[each_cluster] += 1
print()

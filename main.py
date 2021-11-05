import time
import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from sklearn.mixture import GaussianMixture

import config
import src.data_load as loader
from src.preprocessing import mecab_token
from src.call_back import CustomCallback

########################################################################################################################
# config
########################################################################################################################
stopwords = config.stopwords
gmm_components = config.gmm_components

########################################################################################################################
# Data Loading
########################################################################################################################
comments = loader.comments

########################################################################################################################
# Preprocess
########################################################################################################################
print('Tokenization start')
start = time.time()
tokenized_comments, token_frequency, token_frequency_sentencewise = mecab_token(comments)
print(f'Duration: {time.time() - start}')

########################################################################################################################
# Model(W2V, GMM) training
########################################################################################################################
print('W2V start')
start = time.time()
model_embedding = Word2Vec(tokenized_comments, vector_size=1024, compute_loss=True, seed=1246, epochs=5, sg=1,
                           hs=0, alpha=1e-2, callbacks=[CustomCallback()])
print(f'Duration: {time.time() - start}')
# model_embedding.save('result/total/w2v_model.model')

# model_embedding = Word2Vec.load('result/total/w2v_model.model')
embeddings = model_embedding.wv.vectors
print('GMM start')
start = time.time()
model_clustering = GaussianMixture(n_components=gmm_components, random_state=1246).fit_predict(embeddings)
print(f'Duration: {time.time() - start}')

########################################################################################################################
# Hierarchical clustering : 일부 클러스터에 많이 모여있는 것을 다시 clustering.
########################################################################################################################
voca = np.array(model_embedding.wv.index_to_key)
voca_clusters = {}

for i in range(gmm_components):
    voca_clusters[i] = voca[model_clustering == i]

# 현잰 3,4번에 많이 모여있는 것으로 판단.
parent_clusters = [3, 4]
child_components = 10
parentwise_child_clustering = {}

for parent_cluster_idx in parent_clusters:
    print(f'{parent_cluster_idx}th cluster : GMM start')
    start = time.time()
    parent_cluster_voca = voca_clusters[parent_cluster_idx]
    parent_cluster_embedding = embeddings[model_clustering == parent_cluster_idx]
    child_clustering = GaussianMixture(n_components=child_components, random_state=1246).fit_predict(parent_cluster_embedding)
    parentwise_child_clustering[parent_cluster_idx] = child_clustering
    # np.savetxt(f'result/total/{parent_cluster_idx}th_child_cluster.txt', child_clustering)
    # child_clusters = [parent_cluster_voca[child_clustering == i] for i in range(child_components)]
    print(f'Duration: {time.time() - start}')

for parent_cluster_idx in parent_clusters:
    past_cluster = voca_clusters.pop(parent_cluster_idx)
    parent_cluster = np.loadtxt(f'result/total/{parent_cluster_idx}th_child_cluster.txt')
    parent_cluster_types = np.unique(parent_cluster)
    for parent_cluster_type in parent_cluster_types:
        voca_clusters[int(str(parent_cluster_idx)+str(int(parent_cluster_type)))] = past_cluster[parent_cluster==parent_cluster_type]

voca_dictionary = {}
for token_cluster_idx, cluster_contents in voca_clusters.items():
    for cluster_content in cluster_contents:
        voca_dictionary[cluster_content] = token_cluster_idx

########################################################################################################################
# Save : W2V model / token list / cluster별 token / token-cluster matching
########################################################################################################################
model_embedding.save('result/total/w2v_model.model')

# f = open('result/total/voca.txt', 'a', encoding="UTF-8-sig")
# for voca in model_embedding.wv.index_to_key:
#     f.write(f'{voca}\n')
# f.close()
#
# for idx, tokens in voca_clusters.items():
#     file = open(f'result/total/cluster_{idx}.txt', 'a', encoding="UTF-8-sig")
#     for token in tokens:
#         file.write(f'{token}\n')
#     file.close()

token_cluster = pd.DataFrame(columns=['Token', 'Cluster'])
for token, cluster_idx in voca_dictionary.items():
    current = pd.DataFrame([token, cluster_idx], columns=['Token', 'Cluster'])
    token_cluster = pd.concat((token_cluster, ), axis=0)
token_cluster.to_csv('result/token_cluster.csv')

print()

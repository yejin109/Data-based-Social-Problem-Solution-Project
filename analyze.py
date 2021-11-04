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


voca_clusters = [voca[model_clustering == i] for i in range(gmm_components)]
similarity_clusters = [cosine_similarity(embeddings[model_clustering == i]) for i in range(gmm_components)]

cluster_bias = []
token_bias = []
for similarity_cluster in similarity_clusters:
    np.fill_diagonal(similarity_cluster, 0)
    cluster_bias.append(np.sum(similarity_cluster)/(similarity_cluster.shape[0]*(similarity_cluster.shape[0]-1)))

    token_bias_cluster = np.average(similarity_cluster, axis=1)
    token_bias.append(token_bias_cluster)

key_score = scoring('페미', cluster_bias, token_bias, voca_clusters)[0][0]

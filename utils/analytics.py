import numpy as np
import pandas as pd

def key_search(key: list, voca_clusters):
    for cluster_idx, voca_cluster in enumerate(voca_clusters):
        check = np.sum(np.isin(voca_cluster, key))
        if check == len(key):
            return cluster_idx
    return '같은 그룹이 아니에요!'


def scoring(key: str, cluster_bias, token_bias, voca_clusters):
    cluster_idx = key_search([key])
    score_cluster = cluster_bias[cluster_idx]
    score_token = token_bias[cluster_idx][np.argwhere(voca_clusters[cluster_idx]==key)]

    score = 50*score_cluster + 10*score_token
    return score


def get_similar_clusters(token, similarity, cluster2token, token2cluster, key: str):
    key_idx = np.argwhere(token == key)[0][0]

    pairwise_distance = similarity[key_idx, :]

    top_idx = np.argsort(pairwise_distance)[::-1][:500]
    top_tokens = token[top_idx]

    cluster_scores = {}
    for voca_cluster_idx in list(cluster2token.keys()):
        cluster_scores[voca_cluster_idx] = 0

    for top_1000_voca in top_tokens:
        each_cluster = token2cluster[top_1000_voca]
        cluster_scores[each_cluster] += 1

    for cluster_score_key, cluster_score_value in cluster_scores.items():
        cluster_scores[cluster_score_key] = [cluster_score_value]

    result = pd.DataFrame.from_dict(cluster_scores)
    result.index = [key]
    return result

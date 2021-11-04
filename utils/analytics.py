import numpy as np


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
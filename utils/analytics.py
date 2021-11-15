import numpy as np
import pandas as pd
from yonsei_social import config


class Analyzer:
    def __init__(self, token, similarity, cluster2token, token2cluster):
        self.token = token
        self.similarity = similarity
        self.cluster2token = cluster2token
        self.token2cluster = token2cluster

    def get_similar_clusters(self, key: str):
        key_type = config.keys_type[key]
        key_idx = np.argwhere(self.token == key)[0][0]

        pairwise_distance = self.similarity[key_idx, :]

        top_idx = np.argsort(pairwise_distance)[::-1][:500]
        top_tokens = self.token[top_idx]

        cluster_scores = {}
        for voca_cluster_idx in list(self.cluster2token.keys()):
            cluster_scores[voca_cluster_idx] = 0

        for top_1000_voca in top_tokens:
            each_cluster = self.token2cluster[top_1000_voca]
            cluster_scores[each_cluster] += 1
            # When Normalizing
            # cluster_scores[each_cluster] += 1/len(cluster2token[each_cluster])

        for cluster_score_key, cluster_score_value in cluster_scores.items():
            cluster_scores[cluster_score_key] = [cluster_score_value]

        result = pd.DataFrame.from_dict(cluster_scores)
        result.index = [key]
        result['Type'] = key_type
        return result

    def get_key2cluster_distribution(self, keys, result):
        for key in keys:
            if key not in self.token:
                continue
            result = self.get_similar_clusters(key)
            result = pd.concat((result, result), axis=0)
        return result


# def key_search(key: list, voca_clusters):
#     for cluster_idx, voca_cluster in enumerate(voca_clusters):
#         check = np.sum(np.isin(voca_cluster, key))
#         if check == len(key):
#             return cluster_idx
#     return '같은 그룹이 아니에요!'
#
#
# def scoring(key: str, cluster_bias, token_bias, voca_clusters):
#     cluster_idx = key_search([key])
#     score_cluster = cluster_bias[cluster_idx]
#     score_token = token_bias[cluster_idx][np.argwhere(voca_clusters[cluster_idx]==key)]
#
#     score = 50*score_cluster + 10*score_token
#     return score

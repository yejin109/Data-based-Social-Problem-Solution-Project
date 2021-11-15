import numpy as np
import pandas as pd
from yonsei_social import config
from utils import Tokenizer as tk
from gensim.models import Word2Vec
from yonsei_social.utils.analytics import Analyzer
from sklearn.metrics.pairwise import cosine_similarity


class Detector:
    def __init__(self, threshold=0.001):
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

        similarity = cosine_similarity(embeddings)

        for i in range(similarity.shape[0]):
            similarity[i, i] = 0

        self.analyzer = Analyzer(token, similarity, cluster2token, token2cluster)
        self.thr = threshold
        self.stopwords = config.stopwords

    def get_relevant_clusters(self, key):
        key_idx = np.argwhere(self.analyzer.token == key)[0][0]

        pairwise_distance = self.analyzer.similarity[key_idx, :]

        top_idx = np.argsort(pairwise_distance)[::-1][:500]
        top_tokens = self.analyzer.token[top_idx]

        cluster_scores = {}
        for voca_cluster_idx in list(self.analyzer.cluster2token.keys()):
            cluster_scores[voca_cluster_idx] = 0

        for top_1000_voca in top_tokens:
            each_cluster = self.analyzer.token2cluster[top_1000_voca]
            cluster_scores[each_cluster] += 1

        for cluster_score_key, cluster_score_value in cluster_scores.items():
            cluster_scores[cluster_score_key] = [cluster_score_value]

        result = pd.DataFrame.from_dict(cluster_scores)
        result.index = [key]
        return result

    def get_cluster_distribution(self, sentences):
        """
        :param sentences: nested list eg. [ [token1, token2, ..., ] [sentence2], ...]
        :return: score distribution
        """
        overall_result = pd.DataFrame(columns=list(self.analyzer.cluster2token.keys()))
        for sentence_idx, sentence in enumerate(sentences):
            for key in sentence:
                relevant_cluster_table = self.get_relevant_clusters(key).iloc[0, :]
                relevant_cluster_probs = np.exp(relevant_cluster_table.values)/np.sum(np.exp(relevant_cluster_table.values))
                overall_result[sentence_idx] = relevant_cluster_probs

        return overall_result

    def get_tokenized(self, sentences):
        print('Mecab Tokenization has just started!')
        tokenized_sentence = []
        for sentence in sentences:
            if str(sentence) == 'nan':
                continue
            tokens = tk.tokenizer(sentence)
            filt = []
            for token in tokens:
                if token not in self.stopwords:
                    filt.append(token)
            tokenized_sentence.append(filt)
        return tokenized_sentence

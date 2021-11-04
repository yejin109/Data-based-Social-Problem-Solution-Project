import time
import numpy as np

from gensim.models import Word2Vec
from sklearn.mixture import GaussianMixture

import config
import src.data_load as loader
from src.preprocessing import mecab_token
from src.call_back import CustomCallback

# config
stopwords = config.stopwords
gmm_components = config.gmm_components

# Data Loading
comments = loader.comments

# Preprocess
print('Tokenization start')
start = time.time()
tokenized_comments, token_frequency, token_frequency_sentencewise = mecab_token(comments)
print(f'Duration: {time.time() - start}')

# Model(W2V, GMM) training
print('W2V start')
start = time.time()
mode_embedding = Word2Vec(tokenized_comments, vector_size=256, compute_loss=True, seed=1246, epochs=5, sg=1,
                          hs=0, alpha=1e-2, callbacks=[CustomCallback()])
mode_embedding.save('result/total/w2v_model.model')
embeddings = mode_embedding.wv.vectors
print(f'Duration: {time.time() - start}')

print('GMM start')
start = time.time()
model_clustering = GaussianMixture(n_components=gmm_components, random_state=1246).fit_predict(embeddings)
print(f'Duration: {time.time() - start}')

np.savetxt('result/total/embeddings.txt', embeddings)
np.savetxt('result/total/clustered.txt', model_clustering)
f = open('result/total/voca.txt', 'a', encoding="UTF-8-sig")
for voca in mode_embedding.wv.index_to_key:
    f.write(f'{voca}\n')
f.close()

print()

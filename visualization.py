import time
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

import config
from gensim.models import Word2Vec

# config
target_words = config.target_words
font = config.font

# Visualization
model_embedding = Word2Vec.load('result/total/w2v_model.model')
embeddings = np.loadtxt('result/total/embeddings.txt')
model_clustering = np.loadtxt('result/total/clustered.txt')
f = open('result/total/voca.txt', 'r', encoding='UTF8')
voca = []
while True:
    line = f.readline()
    if not line: break
    voca.append(line)
f.close()

print('TSNE start')
start = time.time()
model_tsne = TSNE(random_state=1246).fit_transform(embeddings)
print(f'Duration: {time.time() - start}')

print('PLOT start')
start = time.time()
plt.figure()
plt.scatter(model_tsne[:, 0], model_tsne[:, 1], c=model_clustering, s=1)
for target_word in target_words:
    try:
        target_idx = model_embedding.wv.key_to_index[target_word]
        target_x = model_tsne[target_idx, 0]
        target_y = model_tsne[target_idx, 1]
        plt.annotate(font[target_word], xy=(target_x, target_y), fontsize=30)
    except:
        continue
print(f'Duration: {time.time() - start}')
plt.savefig('result/total/clustering.png')
plt.show()

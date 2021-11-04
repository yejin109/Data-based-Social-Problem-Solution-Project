import glove.corpus as cp
import glove.glove as gl


def init(texts):
    corpus = cp.Corpus()
    corpus.fit(texts, window=5)
    return corpus


def glv(corpus, keyword: str, lr=0.05):
    glove = gl.Glove(no_components=100, learning_rate=lr)
    glove.fit(corpus.matrix, epochs=20, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    model_result = glove.most_similar(keyword)
    return model_result




from gensim.models import Word2Vec


def sim_words(texts, keyword: str):
    model = Word2Vec(sentences=texts, vector_size=50, window=5, min_count=5, workers=4, sg=0)
    voc = model.wv.index_to_key
    model_result = model.wv.most_similar(keyword)
    return model_result

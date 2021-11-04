import pandas as pd
from gensim import corpora
import gensim
import pyLDAvis.gensim_models


num_topic = 20


def lda(subtitles, show_all=False):
    print('step 1')
    dictionary = corpora.Dictionary(subtitles)
    print('step 2')
    corpus = [dictionary.doc2bow(text) for text in subtitles]

    print('step 3')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topic, id2word=dictionary, passes=15)
    print('step 4')
    topics = ldamodel.print_topics(num_words=4)
    if show_all:
        for i in ldamodel.print_topics():
            print(i)
    else:
        for topic in topics:
            print(topic)


def lda_visualization(subtitles):
    print('step 1')
    dictionary = corpora.Dictionary(subtitles)
    print('step 2')
    corpus = [dictionary.doc2bow(text) for text in subtitles]
    print('step 3')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topic, id2word=dictionary, passes=15)

    # pyLDAvis.enable_notebook()
    print('step 4')
    vis = pyLDAvis.gensim_models.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.save_html(vis, 'LDA_Vis2.html')
    # pyLDAvis.display(vis)


def make_topictable_per_doc(ldamodel, corpus):
    topic_table = pd.DataFrame()

    for i, topic_list in enumerate(ldamodel[corpus]):
        doc = topic_list[0] if ldamodel.per_word_topics else topic_list
        doc = sorted(doc, key=lambda x: (x[1]), reverse=True)

        for j, (topic_num, prop_topic) in enumerate(doc):
            if j == 0:
                topic_table = topic_table.append(pd.Series([int(topic_num), round(prop_topic, 4), topic_list]),
                                                 ignore_index=True)
            else:
                break
    return topic_table


def topic_per_doc(subtitles):
    dictionary = corpora.Dictionary(subtitles)
    corpus = [dictionary.doc2bow(text) for text in subtitles]
    num_topic = 20
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topic, id2word=dictionary, passes=15)

    topictable = make_topictable_per_doc(ldamodel, corpus)
    topictable = topictable.reset_index()  # 문서 번호을 의미하는 열(column)로 사용하기 위해서 인덱스 열을 하나 더 만든다.
    topictable.columns = ['문서 번호', '가장 비중이 높은 토픽', '가장 높은 토픽의 비중', '각 토픽의 비중']

    return topictable

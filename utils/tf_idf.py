# DEPRECATED
# def tf(voca: list, subtitles: list):
#     n = len(voca)
#     tf_table = np.zeros(n).reshape(1, n)
#     vocab = np.array(voca)
#     for subtitle in subtitles:
#         palette = np.zeros(n)
#         for token in subtitle:
#             count = subtitle.count(token)
#             palette[vocab == token] = count
#         tf_table = np.vstack((tf_table, palette))
#
#     return tf_table[1:]
#
#
# def idf(voca: list, subtitles: list):
#     n = len(voca)
#     voca = np.array(voca)
#     count = 0
#     palette = np.zeros(n)
#     for vocab in voca:
#         for subtitle in subtitles:
#             if vocab in subtitle:
#                 count += 1
#         palette[voca == vocab] = count
#         count = 0
#
#     palette = np.array(palette)
#     idf_table = np.log(len(subtitles)/(1+palette))
#
#     return idf_table


def get_topics(components, feature_names, n=5):
    for idx, topic in enumerate(components):
        print("Topic %d:" % (idx+1), [(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-n - 1:-1]])

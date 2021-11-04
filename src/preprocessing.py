import numpy as np
import pandas as pd
import Settings as sets
from utils import Tokenizer as tk


def mecab_token(texts):
    stopwords = sets.stopwords
    print('Mecab Tokenization has just started!')
    tokenized_sentence = []
    voca = {}
    term_freq = {}
    term_freq_list = []
    for sentence in texts:
        if str(sentence)=='nan':
            continue
        tokens = tk.tokenizer(sentence)
        filt = []
        for token in tokens:
            if token not in stopwords:
                filt.append(token)
                if token not in voca:
                    voca[token] = 0
                voca[token] += 1
                term_freq[token] = sentence.count(token)
        term_freq_list.append(term_freq)
        term_freq = {}
        tokenized_sentence.append(filt)

    print(f'Voca Size : {len(voca)}')
    return tokenized_sentence, voca, term_freq_list


# vocabulary process
def vocabing(voca):
    voca_sorted = sorted(voca.items(), key=lambda x: x[1], reverse=True)
    word_dict = {}
    voca_set = {}
    i = 0
    j = 0
    for (word, frequency) in voca_sorted:
        voca_set[word] = j
        j += 1
        if frequency > 1:
            i += 1
            word_dict[word] = i

    word_dict['OOV'] = len(word_dict) + 1
    return voca_sorted, word_dict, voca_set


def encoding(sentences, word_dict):
    enco = []
    padd = np.zeros((len(sentences), len(word_dict)), dtype=int)
    # Integer Encoding
    for tokens in sentences:
        temp = []
        for token in tokens:
            try:
                temp.append(word_dict[token])
            except KeyError:
                temp.append(word_dict['OOV'])
        enco.append(temp)

    # Padding
    for i in range(len(enco)):
        on_encoding = enco[i]
        for j in range(len(on_encoding)):
            padd[i, j] = on_encoding[j]
    # for item in enco:
    #     while len(item) < max_len:
    #         item.append(0)

    return padd


def cleaner(text: pd.Series):
    text = text.str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    text = text.str.replace('^ +', "")
    text = text.replace('', np.nan)
    text.drop_duplicates(inplace=True)
    text.dropna(inplace=True)
    return text

# # Nate Pan
# comments = pd.read_csv('../data/nate_pan/comments_nate_pan.csv', index_col=0)
# comments = comments.iloc[:, 0]
# tokenized, token_count, token_count_commentwise = mecab_token(comments)
# token_count_sorted, _, token_idx = vocabing(token_count)
#
#
# t_comments = []
# for t_comment in tokenized:
#     comment = ''
#     for token in t_comment:
#         comment += token + ' / '
#     t_comments.append(comment)
#
#
# tokenized = pd.DataFrame(t_comments)
# tokenized.to_csv('../data/nate_pan/tokenized_comments.csv')
#
# token_idx = pd.DataFrame(token_idx, index=['Index'])
# token_idx.to_csv('../data/nate_pan/token_idx.csv')
#
# token_count = pd.DataFrame(token_count, index=['Frequency'])
# token_count.to_csv('../data/nate_pan/token_count.csv')

# # FM Korea
# comments = pd.read_csv('../result/FMkorea/keyword1_페미/key_comments.csv', index_col=0)
# comments = comments.iloc[:, 0]
# comments.dropna(inplace=True)
# start = time.time()
# tokenized, token_count, token_count_commentwise = mecab_token(comments)
# token_count_sorted, _, token_idx = vocabing(token_count)
# print(f'Tokenizing Duration : {time.time() - start}')
#
# tf = np.zeros((len(tokenized), len(token_idx)))
# for i in range(len(token_count_commentwise)):
#     start = time.time()
#     token_dist = token_count_commentwise[i]
#     for j in token_dist.keys():
#         tf[i, token_idx[j] - 1] = token_dist[j]
#     if i % 10000 == 0:
#         print(f'Process: {i}/{len(tokenized)} / Duration: {time.time() - start}')
#
# t_comments = []
# for i, t_comment in enumerate(tokenized):
#     start = time.time()
#     comment = ''
#     for token in t_comment:
#         comment += token + ' / '
#     t_comments.append(comment)
#     if i % 10000 == 0:
#         print(f'Process: {i}/{len(tokenized)} / Duration: {time.time() - start}')
#
#
# tokenized = pd.DataFrame(t_comments)
# tokenized.to_csv('../data/FMkorea/key_tokenized_comments.csv')
# print('DONE')
# tokenized = None
#
# token_idx = pd.DataFrame(token_idx, index=['Index'])
# token_idx.to_csv('../data/FMkorea/key_token_idx.csv')
# print('DONE')
# token_idx = None
#
# token_count = pd.DataFrame(token_count, index=['Frequency'])
# token_count.to_csv('../data/FMkorea/key_token_count.csv')
# print('DONE')
# token_count = None
#
# np.savetxt('../data/FMkorea/key_tf_table.txt', tf)
# print('DONE')
# print()

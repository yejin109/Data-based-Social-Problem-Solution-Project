import MeCab as mc
import re
from konlpy.tag import Mecab

# tokenizer = Mecab(dicpath='C:/mecab/mecab-ko-dic')
mecab = mc.Tagger(f"--dicdir C:\mecab\mecab-ko-dic")

k = re.compile('ㅋ*')
z = re.compile('ㅉ*')
u = re.compile('ㅜ*')
w = re.compile('ㅠ*')

# target_pos = ['NNG', 'NNP']
target_pos = ['NNG', 'NNP', 'VV', 'VA', 'VCP', 'VCN', 'XR']


def tokenizer(t):
    text = t
    text_lengths = 0
    tokenized = []
    for mor in mecab.parse(text).split("\n"):
        if "\t" in mor:
            splitted = mor.split("\t")
            token = splitted[0]

            # 품사를 구분하여 사용할 것이라면 아래의 코드를 사용하도록 하자.
            pos = splitted[1].split(",", 1)[0]
            if pos.find('+') != -1:
                post_splited = pos.split('+')
                if post_splited not in target_pos:
                    continue
                else:
                    tokenized.append(token)
                    text_lengths += 1
            else:
                if pos not in target_pos:
                    continue
                else:
                    tokenized.append(token)
                    text_lengths += 1
            # if text[text_ptr] == " ":
            #     while text[text_ptr] == " ":
            #         text_ptr += 1
            #     assert (
            #             text[text_ptr] == token[0]
            #     ), f"{repr(text)}//{text_ptr}//{text[text_ptr]}//{token}//{token[0]}\n"

            # tokenized.append(token)
            # text_ptr += len(token)
            # if k.match(token).group() == '':
            #     if z.match(token).group() == '':
            #         if u.match(token).group() == '':
            #             if w.match(token).group() == '':
            #                 tokenized.append(token)
            #                 text_lengths += 1

    return tokenized

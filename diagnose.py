import config
import pandas as pd
from yonsei_social.utils.diasnosis import Detector

aaa = pd.read_csv('result/key_result.csv', index_col=0)
stopwords = config.stopwords
detector = Detector()

# 검사할 문장
sentences = [
    ['인터넷과 현실의 자아가 동일하지 못하는게 그거 이중자아다중이고 현실에선 이랬지만 온라인에선 이래야지 이러는게 정신병임'],
    ['니 와꾸가 제일 음침해 난 남자한테 까이기만 해서 커플 후려칠거야 못생겨서 연애 못하는거 아니거든']
]

# Tokenize
tokenized = detector.get_tokenized(sentences)

# Diagnose
test = detector.get_cluster_distribution(tokenized)

print()
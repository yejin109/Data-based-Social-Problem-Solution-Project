import config
import pandas as pd
from src.preprocessing import cleaner

comments_n1 = pd.read_csv('data/nate_pan/comments_nate_pan.csv', index_col=0, header=0)
comments_n1 = cleaner(comments_n1.iloc[:, 0])
comments_n2 = pd.read_csv('data/nate_pan/comments_nate_pan_페미.csv', index_col=0, header=0)
comments_n2 = cleaner(comments_n2.iloc[:, 0])
# comments_f1 = pd.read_csv('data/FMkorea/comments_fmkorea.csv', index_col=0, header=0)
# comments_f1 = cleaner(comments_f1.iloc[:, 0])
comments_f2 = pd.read_csv('data/FMkorea/comments_fmkorea_key1.csv', index_col=0, header=0)
comments_f2 = cleaner(comments_f2.iloc[:, 0])
comments_f3 = pd.read_csv('data/FMkorea/comments_fmkorea_key2.csv', index_col=0, header=0)
comments_f3 = cleaner(comments_f3.iloc[:, 0])
comments = pd.concat([comments_n2, comments_f2, comments_f3])

# '군무새', '남혐', '여시', '여혐', '열폭', '찐따', '취집', '탈코', '트페미', '페미', '한남', '할당제'
search_keys = config.search_keys
for search_key in search_keys:
    comments_search_key = pd.read_csv(f'data/nate_pan/comments_nate_pan_{search_key}.csv', index_col=0, header=0)
    comments_search_key = cleaner(comments_search_key.iloc[:, 0])
    comments = pd.concat([comments, comments_search_key])

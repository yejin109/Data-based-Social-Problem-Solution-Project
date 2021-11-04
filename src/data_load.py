import pandas as pd
from preprocessing import cleaner

comments_n1 = pd.read_csv('data/nate_pan/comments_nate_pan.csv', index_col=0, header=0)
comments_n1 = cleaner(comments_n1.iloc[:, 0])
comments_n2 = pd.read_csv('data/nate_pan/comments_nate_pan_key1.csv', index_col=0, header=0)
comments_n2 = cleaner(comments_n2.iloc[:, 0])
comments_f1 = pd.read_csv('data/FMkorea/comments_fmkorea.csv', index_col=0, header=0)
comments_f1 = cleaner(comments_f1.iloc[:, 0])
comments_f2 = pd.read_csv('data/FMkorea/comments_fmkorea_key1.csv', index_col=0, header=0)
comments_f2 = cleaner(comments_f2.iloc[:, 0])
comments_f3 = pd.read_csv('data/FMkorea/comments_fmkorea_key2.csv', index_col=0, header=0)
comments_f3 = cleaner(comments_f3.iloc[:, 0])

comments = pd.concat([comments_n1, comments_n2, comments_f1, comments_f2, comments_f3])

import pandas as pd
import numpy as np

comments = pd.Series([])

comments_key = pd.read_csv(f'../data/FMkorea/comments_fmkorea_key2_raw.csv', header=0, index_col=0)

for column in range(comments_key.columns.size):
    line = comments_key.iloc[:, column]
    line.dropna(inplace=True)
    line.drop_duplicates(inplace=True)
    comments = pd.concat([comments, line])

# for thread_idx in range(7):
#     comments_idx = pd.read_csv(f'../data/nate_pan/comments_{thread_idx}.csv', header=0, index_col=0)
#     for column in comments_idx.columns:
#         line = comments_idx[column]
#         line = line.dropna()
#         line = line.drop_duplicates()
#         comments = pd.concat([comments, line])
# comments.dropna(inplace=True)

mask_numeric = comments.str.isnumeric()
print(f'Numeric : {np.sum(mask_numeric)}')
comments = comments[~mask_numeric]
comments.dropna(inplace=True)

comments = comments.str.replace("\W", '')
comments = comments.str.replace(" ", '')
mask_space= comments.str.isspace()
print(f'Space: {np.sum(mask_space)}')
comments = comments[~mask_space]
comments.dropna(inplace=True)

comments.to_csv('../data/FMkorea/comments_fmkorea_key2.csv')
print()

import numpy as np
import pandas as pd


def peelingHTML(text):
    filted = text.str.replace(pat='<br />', repl=r'')
    filted = filted.str.replace(pat='<br>', repl=r'')
    filted = filted.str.replace(pat='<b>', repl=r'')
    filted = filted.str.replace(pat='</b>', repl=r'')
    filted = filted.str.replace(pat='</a>', repl=r'')
    filted = filted.str.replace(pat='</i>', repl=r'')
    filted = filted.str.replace(pat='<i>', repl=r'')
    filted = filted.str.replace(pat='&quot', repl=r'')
    # filted = filted.str.replace(pat=r'[^\w]', repl=r'', regex=True)
    return filted

# na_filt = symbol_filt.replace('', np.nan)
# na_filt = na_filt.dropna()


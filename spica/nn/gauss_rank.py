from itertools import accumulate

import numpy as np
import pandas  as pd
from scipy.special import erfinv
from scipy.stats import rankdata
from tqdm import tqdm


def gauss_rank(dfs, cols=None, null_value=np.nan, fill_value=0, eps=0.01):
    df = pd.concat(dfs, axis=0)  # type: pd.DataFrame
    cols = cols or df.columns
    for f in tqdm(cols):
        null = df[f] == null_value
        d = df.loc[df[f] != null_value, f]
        df.loc[null, f] = fill_value
        df.loc[~null, f] = erfinv((rankdata(d) - 1) / len(d) * 2 * (1 - eps) - (1 - eps))
    
    res = []
    lens = list(accumulate([0] + [len(df) for df in dfs]))
    for start, end in zip(lens, lens[1:]):
        res.append(df[cols][start:end].copy())
    if len(res) == 1:
        return res[0]
    else:
        return res

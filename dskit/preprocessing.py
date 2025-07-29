import numpy as np
import pandas as pd


def merge_rare_values(series: pd.Series, threshold: float = 0.01, default: str = 'OTHER') -> pd.Series:
    abs_f = series.value_counts(dropna=False) / len(series)

    top_values = abs_f[abs_f >= threshold].index.tolist()

    return pd.Series(index=series.index, data=np.where(series.isin(top_values), series, default))


def qcut_enumerate_float(x: pd.Series, q=10) -> pd.Series:
    t = pd.qcut(x, q=q)

    bins = t.value_counts(dropna=False).index.sort_values().tolist()

    d = {b: i for i, b in enumerate(bins, start=1)}

    t = t.map(d)

    if np.nan in d:
        return t.cat.add_categories(0).fillna(0)
    else:
        return t

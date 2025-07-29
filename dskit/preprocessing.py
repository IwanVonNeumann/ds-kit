import numpy as np
import pandas as pd


def merge_rare_values(series: pd.Series, threshold: float = 0.01, default: str = 'OTHER') -> pd.Series:
    abs_f = series.value_counts(dropna=False) / len(series)

    top_values = abs_f[abs_f >= threshold].index.tolist()

    return pd.Series(index=series.index, data=np.where(series.isin(top_values), series, default))


def enumerate_qcut(x: pd.Series, q=10, process_zeros: bool = False) -> pd.Series:
    if process_zeros:
        x_0 = x[x == 0]
        x = x[x != 0]
    else:
        x_0 = pd.Series()

    t = pd.qcut(x, q=q)

    bins = t.value_counts(dropna=False).index.sort_values().tolist()

    d = {b: b.left for i, b in enumerate(bins, start=1)}

    t = t.map(d)

    if process_zeros:
        t = pd.concat(objs=[x_0, t])

    if np.nan in d:
        return t.cat.add_categories(0).fillna(0)
    else:
        return t

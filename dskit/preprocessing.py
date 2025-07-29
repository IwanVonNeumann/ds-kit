import numpy as np
import pandas as pd


def merge_rare_values(series: pd.Series, threshold: float = 0.01, default: str = 'OTHER') -> pd.Series:
    abs_f = series.value_counts(dropna=False) / len(series)

    top_values = abs_f[abs_f >= threshold].index.tolist()

    return pd.Series(index=series.index, data=np.where(series.isin(top_values), series, default))

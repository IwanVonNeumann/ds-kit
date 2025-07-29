from typing import Optional

import pandas as pd

from pandas.io.formats.style import Styler


def check_empty_values(df: pd.DataFrame, col: str):
    n = len(df)
    n_nans = df[col].isna().sum()
    n_zeros = (df[col] == 0).sum()

    print('nans:  {} ({:.1%})'.format(n_nans, n_nans / n))
    print('zeros: {} ({:.1%})'.format(n_zeros, n_zeros / n))


def __thousand_separators(x):
    return '{:,}'.format(x).replace(',', ' ')


def get_target_pivot(df: pd.DataFrame, col: str, target_col: str, revenue_col: Optional[str] = None) -> Styler:
    grouped_df = df.groupby(col, observed=True)

    n_count_col = 'n_items'
    p_count_col = '%_items'
    p_revenue_col = None

    summary = grouped_df[target_col].agg([
        (target_col, 'mean'),
        (n_count_col, 'count')
    ]).reset_index()

    summary[p_count_col] = summary[n_count_col] / len(df)

    target_by_row = summary[target_col] * summary[n_count_col]

    if revenue_col is not None:
        p_revenue_col = '%_rev'

        summary[p_revenue_col] = target_by_row / target_by_row.sum()

        summary = summary.set_index(col)

    if df[col].dtype == 'object':
        summary = summary.sort_values(by=target_col, ascending=False)
    else:
        summary = summary.sort_index()

    if summary.index.dtype == 'float':
        summary.index = summary.index.map('{:.3f}'.format)

    cols_format = {
        target_col: '{:.2f}'.format,
        n_count_col: __thousand_separators,
        p_count_col: '{:.1%}'.format,
    }

    if revenue_col is not None:
        cols_format[p_revenue_col] = '{:.1%}'.format

    return summary.style.format(cols_format).background_gradient(axis=0, subset=[target_col], cmap='RdYlGn')

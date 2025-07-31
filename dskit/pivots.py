import pandas as pd

from .config import get_target

from typing import Optional, Union
from pandas.io.formats.style import Styler


def check_empty_values(df: pd.DataFrame, col: str):
    n = len(df)
    n_nans = df[col].isna().sum()
    n_zeros = (df[col] == 0).sum()

    print('nans:  {} ({:.1%})'.format(n_nans, n_nans / n))
    print('zeros: {} ({:.1%})'.format(n_zeros, n_zeros / n))


def __thousand_separators(x: Union[float, int]):
    return '{:,}'.format(x).replace(',', ' ')


def get_target_pivot(df: pd.DataFrame, col: str, target_col: Optional[str] = None,
                     revenue_col: Optional[str] = None, positive_target: bool = True) -> Styler:
    if target_col is None:
        target_col = get_target()

    grouped_df = df.groupby(col, observed=True)

    n_count_col = 'n_items'
    p_count_col = '%_items'
    p_revenue_col = None

    summary = grouped_df[target_col].agg([
        (target_col, 'mean'),
        (n_count_col, 'count')
    ]).reset_index()

    summary[p_count_col] = summary[n_count_col] / len(df)

    summary.set_index(col, drop=True, inplace=True)

    if revenue_col is not None:
        p_revenue_col = '%_{}'.format(revenue_col)

        revenue_pivot = df[[col, revenue_col]].groupby(by=col).sum()[revenue_col]

        summary[revenue_col] = revenue_pivot
        summary[p_revenue_col] = revenue_pivot / revenue_pivot.sum()

    sort_order = not positive_target

    if df[col].dtype == 'object':
        summary = summary.sort_values(by=target_col, ascending=sort_order)
    else:
        summary = summary.sort_index(ascending=sort_order)

    cols_format = {
        target_col: '{:.2f}'.format,
        n_count_col: __thousand_separators,
        p_count_col: '{:.1%}'.format,
    }

    if revenue_col is not None:
        cols_format[revenue_col] = '{:.2f}'.format
        cols_format[p_revenue_col] = '{:.1%}'.format

    if summary.index.dtype == 'float':
        summary.index = summary.index.map('{:.3f}'.format)

    if positive_target:
        gradient = 'RdYlGn'
    else:
        gradient = 'RdYlGn_r'

    return summary.style.format(cols_format).background_gradient(axis=0, subset=[target_col], cmap=gradient)

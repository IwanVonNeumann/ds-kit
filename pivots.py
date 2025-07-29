import pandas as pd


def check_empty_values(df: pd.DataFrame, col: str):
    n = len(df)
    n_nans = df[col].isna().sum()
    n_zeros = (df[col] == 0).sum()

    print('nans:  {} ({:.1%})'.format(n_nans, n_nans / n))
    print('zeros: {} ({:.1%})'.format(n_zeros, n_zeros / n))

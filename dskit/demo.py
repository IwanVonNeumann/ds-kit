import numpy as np
import pandas as pd


def generate_demo_df(size: int) -> pd.DataFrame():
    df = pd.DataFrame()

    df['client_class'] = np.random.choice(['A', 'B', 'C'], p=[0.05, 0.15, 0.8], size=size)

    index_a = df[df['client_class'] == 'A'].index
    index_b = df[df['client_class'] == 'B'].index
    index_c = df[df['client_class'] == 'C'].index

    n_a = len(index_a)
    n_b = len(index_b)
    n_c = len(index_c)

    df.loc[index_a, 'total_payments'] = np.random.normal(loc=20_000, scale=5_000, size=n_a)
    df.loc[index_b, 'total_payments'] = np.random.normal(loc=5_000, scale=2_000, size=n_b)
    df.loc[index_c, 'total_payments'] = np.random.normal(loc=1_000, scale=250, size=n_c)

    df.loc[index_a, 'risk'] = np.random.choice([0, 1], p=[0.95, 0.05], size=n_a)
    df.loc[index_b, 'risk'] = np.random.choice([0, 1], p=[0.90, 0.10], size=n_b)
    df.loc[index_c, 'risk'] = np.random.choice([0, 1], p=[0.80, 0.20], size=n_c)

    return df

from pathlib import Path

import pandas as pd

import settings


def _filter_dataset(df, geocodes):
    return df[df.iloc[:, 0].str.contains('|'.join(geocodes), regex=True)]


def _clean_dataset(df):
    def clean_values(series):
        series = series.str.replace(r'[ a-zA-Z:]+$', '', regex=True)
        series = series.replace('.', ',')
        return series

    df = df.apply(lambda series: series.str.strip())
    id_columns = [c.rstrip('\\time').title() for c in df.columns[0].split(',')]
    id_df = df.iloc[:, 0].str.split(',', expand=True)
    id_df.columns = id_columns
    df = df.drop(df.columns[0], axis=1)
    df = df.apply(clean_values)
    return pd.concat([id_df, df], axis=1, verify_integrity=True)


def stage_dataset(dataset: Path, geocodes: list = settings.TARGET_GEOCODES):
    '''Filter & clean dataset taking into account only records with geocodes'''

    df = pd.read_csv(dataset, sep='\t')
    df = _filter_dataset(df, geocodes)
    df = _clean_dataset(df)
    df.to_csv(dataset, index=False, sep='\t')

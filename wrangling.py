from pathlib import Path

import pandas as pd

import settings


def _filter_dataset(df, geocodes):
    gc_pattern = ',(?:' + '|'.join(geocodes) + ') *$'
    return df[df.iloc[:, 0].str.contains(gc_pattern, regex=True)]


def _clean_dataset(df):
    def clean_values(series):
        series = series.str.replace(r'[ a-zA-Z:]+$', '', regex=True)
        series = series.replace('.', ',')
        return series

    df = df.apply(lambda series: series.str.strip())
    id_columns = [c.replace('\\time', '') for c in df.columns[0].split(',')]
    id_df = df.iloc[:, 0].str.split(',', expand=True)
    id_df.columns = id_columns
    df = df.drop(df.columns[0], axis=1)
    df = df.apply(clean_values)
    return pd.concat([id_df, df], axis=1, verify_integrity=True)


def _recode_dataset(df, codelist: Path, language: str):
    cl = pd.read_csv(codelist)
    mapping = cl.pivot(index='code', columns='cl', values=language).to_dict()
    return df.replace(mapping)


def stage_dataset(
    dataset: Path,
    geocodes: list = settings.TARGET_GEOCODES,
    codelist: Path = Path(settings.CODELIST),
    languages: list = settings.RECODING_LANGUAGES,
):
    '''Filter & clean dataset taking into account only records with geocodes'''

    df = pd.read_csv(dataset, sep='\t')
    df = _filter_dataset(df, geocodes)
    df = _clean_dataset(df)

    output_files = []

    for lang in languages:
        recoded_df = _recode_dataset(df, codelist, lang)
        output_stem = f'{dataset.stem}_{lang.lower()}'
        output_dataset = dataset.with_stem(output_stem)
        recoded_df.to_csv(output_dataset, index=False, sep='\t')
        output_files.append(output_dataset)

    dataset.unlink()
    return output_files

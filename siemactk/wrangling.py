from pathlib import Path

import pandas as pd
from logzero import logger

import settings


def codelists_to_dict(codelists: pd.DataFrame, languages=settings.RECODING_LANGUAGES):
    mapping = {}
    for lang in languages:
        mapping[lang] = {}
        for _, group in codelists.groupby('cl'):
            d = group.pivot(index='code', columns='cl', values=lang).to_dict()
            mapping[lang].update(d)
    return mapping


def _filter_dataset(df: pd.DataFrame, geocodes: list[tuple]):
    filtered_df = pd.DataFrame()
    for geocodes_group in geocodes:
        aux = {}
        for geocode in geocodes_group:
            filtered_rows = df.iloc[:, 0].str.contains(fr'{geocode}\s*$', regex=True)
            aux[sum(filtered_rows)] = df[filtered_rows]
        filtered_rows = aux[max(aux)]
        filtered_df = filtered_df.append(filtered_rows, ignore_index=True)
    return filtered_df


def _clean_dataset(df: pd.DataFrame):
    def clean_values(series):
        series = series.str.replace(r'[ a-zA-Z:]+$', '', regex=True)
        series = series.replace('.', ',')
        return series

    df = df.astype(str)
    df = df.apply(lambda series: series.str.strip())
    df.columns = [c.strip() for c in df.columns]
    id_columns = [c.replace('\\time', '') for c in df.columns[0].split(',')]
    id_df = df.iloc[:, 0].str.split(',', expand=True)
    id_df.columns = id_columns
    df = df.drop(df.columns[0], axis=1)
    df = df.apply(clean_values)
    return pd.concat([id_df, df], axis=1, verify_integrity=True)


def _recode_dataset(df: pd.DataFrame, mapping: dict):
    return df.replace(mapping)


def stage_dataset(
    dataset: Path,
    codelists: dict,
    geocodes: list[tuple] = settings.TARGET_GEOCODES,
    languages: list = settings.RECODING_LANGUAGES,
):
    """Stage dataset. Steps:
    1. Read dataset (csv) into a dataframe.
    2. Filter dataset taking into account only records with geocodes.
    3. Clean dataset dropping NaN and replace dots with commas.
    4. Recode dataset for the indicated languages.
    5. Save dataset as csv (tsv) and json formats.
    """

    df = pd.read_csv(dataset, sep='\t')
    df = _filter_dataset(df, geocodes)
    if df.size == 0:
        logger.error('Dataset has no records with supplied geocodes. Discarding...')
        return False
    df = _clean_dataset(df)

    output_files = []

    for lang in languages:
        recoded_df = _recode_dataset(df, codelists[lang])
        output_stem = f'{dataset.stem}_{lang.lower()}'

        output_file = dataset.with_name(output_stem + '.tsv')
        recoded_df.to_csv(output_file, index=False, sep='\t')
        output_files.append(output_file)

        output_file = dataset.with_name(output_stem + '.json')
        recoded_df.to_json(output_file, orient='records')
        output_files.append(output_file)

    dataset.unlink()
    return output_files

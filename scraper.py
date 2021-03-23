import gzip
import os
import re
from pathlib import Path

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import settings


def get_datasets_urls(target_url):
    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get(target_url)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#gepRegionIndicators .tipTable'))
    )

    items = element.find_elements_by_class_name('tipRow')
    for item in items:
        item_id = item.get_attribute('id')
        dataset_code = re.match(r'tipRow_[\d-]+_(.*)', item_id).group(1)
        dataset_table_url = os.path.join(
            settings.BASE_DATASET_URL, dataset_code + '.tsv.gz'
        )
        yield dataset_table_url


def download_dataset(dataset_url, target_folder='data'):
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)
    r = requests.get(dataset_url)
    filename = re.search(r'filename="(.*).tsv.gz"', r.headers['Content-Disposition']).group(
        1
    )
    f = target_folder / (filename + '.tsv')
    f.write_bytes(gzip.decompress(r.content))
    return f


def clean_dataset(dataset: Path, geocodes: list = settings.TARGET_GEOCODES):
    '''Filter & clean dataset taking into account only records with geocodes'''

    def clean_values(series):
        series = series.str.replace(r'[ a-zA-Z:]+$', '', regex=True)
        series = series.replace('.', ',')
        return series

    df = pd.read_csv(dataset, sep='\t')
    df = df[df.iloc[:, 0].str.contains('|'.join(geocodes), regex=True)]
    df = df.apply(lambda series: series.str.strip())
    id_columns = [c.rstrip('\\time').title() for c in df.columns[0].split(',')]
    id_df = df.iloc[:, 0].str.split(',', expand=True)
    id_df.columns = id_columns
    df = df.drop(df.columns[0], axis=1)
    df = df.apply(clean_values)
    df = pd.concat([id_df, df], axis=1, verify_integrity=True)

    df.to_csv(dataset, index=False, sep='\t')

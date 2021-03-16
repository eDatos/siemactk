import re
import sys
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DATASET_URL = (
    'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
    'BulkDownloadListing?file=data/{dataset_code}.tsv.gz'
)


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
        dataset_table_url = BASE_DATASET_URL.format(dataset_code=dataset_code)
        yield dataset_table_url


def download_dataset(datasets_url, target_folder='data'):
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)
    r = requests.get(dataset_url)
    filename = re.search(r'filename="(.*)"', r.headers['Content-Disposition']).group(1)
    f = target_folder / filename
    f.write_bytes(r.content)


if __name__ == '__main__':
    target_url = sys.argv[1]
    for dataset_url in get_datasets_urls(target_url):
        print(f'Downlading {dataset_url}...')
        download_dataset(dataset_url)
